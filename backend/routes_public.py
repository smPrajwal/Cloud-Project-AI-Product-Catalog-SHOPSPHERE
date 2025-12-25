from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import os
import re
import time
from database.db import get_db
from .utils import get_footer_settings, analyze_sentiment

common_bp = Blueprint('common', __name__)


@common_bp.route('/')
def index():
    print("LOG: Accessing index page")
    db = get_db()
    ads = db.execute('SELECT * FROM advertisements ORDER BY id').fetchall()
    footer = get_footer_settings()
    return render_template('index.html', ads=ads, footer=footer)

@common_bp.route('/health')
def health_check():
    return jsonify({'status': 'ok'}), 200


@common_bp.route('/admin-auth')
def admin_auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return 'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}
    
    # Check env vars (default to admin/admin for dev if missing, but code respects stored values)
    required_user = os.environ.get('ADMIN_USERNAME')
    required_pass = os.environ.get('ADMIN_PASSWORD')

    # Handle potential whitespace issues in env vars
    if required_user: required_user = required_user.strip()
    if required_pass: required_pass = required_pass.strip()
    
    if not required_user or not required_pass:
        return 'Admin credentials not configured', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}

    if auth.username == required_user and auth.password == required_pass:
        session['user_id'] = 'admin'
        session['username'] = 'admin'
        session['is_admin'] = True
        return redirect(url_for('common.index'))
    
    return 'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}

@common_bp.route('/logout')
def logout():
    print(f"LOG: User logout: {session.get('username')}")
    session.clear()
    return redirect(url_for('common.index'))

# --- About & Footer Public ---
@common_bp.route('/about')
def about():
    print("LOG: Accessing About Page")
    db = get_db()
    settings = db.execute('SELECT key, value FROM site_settings WHERE key LIKE "about_%"').fetchall()
    content = {row['key']: row['value'] for row in settings}
    footer = get_footer_settings()
    return render_template('about.html', content=content, footer=footer)



# --- Products Public ---
@common_bp.route('/product/<slug>')
def product_detail(slug):
    print(f"LOG: Viewing product: {slug}")
    db = get_db()
    
    if slug.isdigit():
        product = db.execute('SELECT id FROM products WHERE id = ?', (slug,)).fetchone()
    else:
        search = '%' + '%'.join(slug.split('-')) + '%'
        product = db.execute('SELECT id FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,)).fetchone()
    
    if not product:
        return "Product not found", 404
    
    product_id = product['id']
    
    footer = get_footer_settings()
    return render_template('product.html', product_id=product_id, footer=footer)

@common_bp.route('/api/products', methods=['GET'])
def get_products():
    print(f"LOG: API Get Products. Query: {request.args.get('q')}, Tag: {request.args.get('tag')}")
    query = request.args.get('q')
    tag = request.args.get('tag')
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)
    
    db = get_db()
    
    sql = "SELECT * FROM products WHERE 1=1"
    params = []
    
    if query:
        # Simple search across Name, Desc, and Tags
        search_term = f'%{query}%'
        sql += " AND (name LIKE ? OR description LIKE ? OR id IN (SELECT product_id FROM product_tags WHERE tag_name LIKE ?))"
        params.extend([search_term, search_term, search_term])
    
    if tag:
        sql += " AND id IN (SELECT product_id FROM product_tags WHERE tag_name = ?)"
        params.append(tag)
        
    sql += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor = db.execute(sql, params)
    rows = cursor.fetchall()
    
    # 2. Batch fetch tags (Optimization)
    products = []
    if rows:
        ids = [row['id'] for row in rows]
        placeholders = ','.join('?' * len(ids))
        tags_query = f"SELECT product_id, tag_name FROM product_tags WHERE product_id IN ({placeholders})"
        t_rows = db.execute(tags_query, ids).fetchall()
        
        # Group tags by product_id
        tags_map = {}
        for t in t_rows:
            if t['product_id'] not in tags_map: tags_map[t['product_id']] = []
            tags_map[t['product_id']].append(t['tag_name'])

        for row in rows:
            products.append({
                'id': row['id'],
                'name': row['name'],
                'price': int(row['price']),
                'original_price': int(row['original_price']) if row['original_price'] else None,
                'discount_percent': 0,
                'tags': tags_map.get(row['id'], []),
                'thumbnail_url': row['thumbnail_url']
            })
        
    return jsonify(products)

@common_bp.route('/api/products/<int:id>', methods=['GET'])
def get_product_details(id):
    print(f"LOG: API Get Product Details {id}")
    db = get_db()
    p_cursor = db.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = p_cursor.fetchone()
    
    if not product:
        return jsonify({'error': 'Not found'}), 404
    
    t_cursor = db.execute('SELECT tag_name FROM product_tags WHERE product_id = ?', (id,))
    tags = [row['tag_name'] for row in t_cursor.fetchall()]
    
    r_cursor = db.execute('SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC', (id,))
    reviews = [dict(row) for row in r_cursor.fetchall()]
    
    return jsonify({
        'id': product['id'],
        'name': product['name'],
        'description': product['description'],
        'price': int(product['price']),
        'original_price': int(product['original_price']) if product['original_price'] else None,
        'thumbnail_url': product['thumbnail_url'],
        'tags': tags,
        'reviews': reviews
    })




@common_bp.route('/api/products/<int:id>/reviews', methods=['POST'])
def add_review(id):
    data = request.json
    reviewer = data.get('reviewer', '')
    text = data.get('review_text', '')
    
    if not reviewer:
        return jsonify({'error': 'Review reviewer is required'}), 400
    
    if not text:
        return jsonify({'error': 'Review text is required'}), 400

    sentiment = analyze_sentiment(text)
    
    db = get_db()
    cursor = db.execute('INSERT INTO reviews (product_id, reviewer, review_text, sentiment_score, sentiment_label) VALUES (?, ?, ?, ?, ?)',
               (id, reviewer, text, sentiment['score'], sentiment['label']))
    db.commit()
    
    return jsonify({'message': 'Review added', 'sentiment': sentiment, 'id': cursor.lastrowid})


@common_bp.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    if not session.get('is_admin'):
         return jsonify({'error': 'Admins only'}), 403
         
    db = get_db()
    db.execute('DELETE FROM reviews WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'message': 'Review deleted'})

@common_bp.route('/api/products/<int:id>/recommendations', methods=['GET'])
def get_recommendations(id):
    db = get_db()
    tags_cursor = db.execute('SELECT tag_name FROM product_tags WHERE product_id = ?', (id,))
    current_tags = [row['tag_name'] for row in tags_cursor.fetchall()]
    
    if not current_tags:
        return jsonify([])
        
    placeholders = ','.join('?' * len(current_tags))
    sql = f'''
        SELECT DISTINCT p.*, COUNT(pt.tag_name) as overlap
        FROM products p
        JOIN product_tags pt ON p.id = pt.product_id
        WHERE pt.tag_name IN ({placeholders}) AND p.id != ?
        GROUP BY p.id
        ORDER BY overlap DESC
        LIMIT 5
    '''
    params = current_tags + [id]
    
    rec_cursor = db.execute(sql, params)
    recs = []
    for row in rec_cursor.fetchall():
        recs.append({
            'id': row['id'],
            'name': row['name'],
            'price': int(row['price']),
            'original_price': int(row['original_price']) if row['original_price'] else None,
            'thumbnail_url': row['thumbnail_url']
        })
        
    return jsonify(recs)


