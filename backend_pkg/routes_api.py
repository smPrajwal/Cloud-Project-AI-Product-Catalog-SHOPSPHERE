from flask import Blueprint, request, jsonify, session
from database.db import get_db
from shared_pkg.utils import analyze_sentiment
import os

api_bp = Blueprint('api', __name__)

# --- Advertisements API ---
@api_bp.route('/api/ads', methods=['GET'])
def get_ads():
    print("LOG: API Get Ads")
    db = get_db()
    rows = db.execute('SELECT * FROM advertisements').fetchall()
    return jsonify([dict(row) for row in rows])

# --- Products API ---

@api_bp.route('/api/products', methods=['GET'])
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
        search_term = f'%{query}%'
        sql += " AND (name LIKE ? OR description LIKE ? OR id IN (SELECT product_id FROM product_tags WHERE tag_name LIKE ?))"
        params.extend([search_term, search_term, search_term])
    
    if tag:
        sql += " AND id IN (SELECT product_id FROM product_tags WHERE tag_name = ?)"
        params.append(tag)
        
    if os.environ.get('AZURE_SQL_CONN'):
        sql += " ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        params.extend([offset, limit])
    else:
        sql += " LIMIT ? OFFSET ?"
        params.extend([limit, offset])
    
    cursor = db.execute(sql, params)
    rows = cursor.fetchall()
    
    products = []
    if rows:
        ids = [row['id'] for row in rows]
        placeholders = ','.join('?' * len(ids))
        tags_query = f"SELECT product_id, tag_name FROM product_tags WHERE product_id IN ({placeholders})"
        t_rows = db.execute(tags_query, ids).fetchall()
        
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

@api_bp.route('/api/products/<id_or_slug>', methods=['GET'])
def get_product_details(id_or_slug):
    print(f"LOG: API Get Product Details {id_or_slug}")
    db = get_db()
    
    # Handle Slug vs ID
    product = None
    if str(id_or_slug).isdigit():
        product = db.execute('SELECT * FROM products WHERE id = ?', (id_or_slug,)).fetchone()
    else:
        # Slug search
        search = '%' + '%'.join(id_or_slug.split('-')) + '%'
        product = db.execute('SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,)).fetchone()
    
    if not product:
        return jsonify({'error': 'Not found'}), 404
    
    id = product['id'] # Resolved ID
    
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

@api_bp.route('/api/products/<id_or_slug>/reviews', methods=['POST'])
def add_review(id_or_slug):
    db = get_db()
    # Resolve ID
    if str(id_or_slug).isdigit():
        id = id_or_slug
    else:
        search = '%' + '%'.join(id_or_slug.split('-')) + '%'
        product = db.execute('SELECT id FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,)).fetchone()
        if not product: return jsonify({'error': 'Product not found'}), 404
        id = product['id']

    data = request.json
    reviewer = data.get('reviewer', '')
    text = data.get('review_text', '')
    
    if not reviewer or not text:
        return jsonify({'error': 'Missing data'}), 400

    sentiment = analyze_sentiment(text)
    
    cursor = db.execute('INSERT INTO reviews (product_id, reviewer, review_text, sentiment_score, sentiment_label) VALUES (?, ?, ?, ?, ?)',
               (id, reviewer, text, sentiment['score'], sentiment['label']))
    db.commit()
    
    return jsonify({'message': 'Review added', 'sentiment': sentiment, 'id': cursor.lastrowid})

@api_bp.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    if not session.get('is_admin'):
         return jsonify({'error': 'Admins only'}), 403
         
    db = get_db()
    db.execute('DELETE FROM reviews WHERE id = ?', (id,))
    db.commit()
    
    return jsonify({'message': 'Review deleted'})

@api_bp.route('/api/ads', methods=['GET'])
def get_ads():
    db = get_db()
    rows = db.execute('SELECT * FROM advertisements').fetchall()
    return jsonify([dict(row) for row in rows])

@api_bp.route('/api/products/<id_or_slug>/recommendations', methods=['GET'])
def get_recommendations(id_or_slug):
    db = get_db()
    
    # Resolve ID if slug is passed
    if str(id_or_slug).isdigit():
        id = id_or_slug
    else:
        search = '%' + '%'.join(id_or_slug.split('-')) + '%'
        product = db.execute('SELECT id FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,)).fetchone()
        if not product: return jsonify([])
        id = product['id']

    tags_cursor = db.execute('SELECT tag_name FROM product_tags WHERE product_id = ?', (id,))
    current_tags = [row['tag_name'] for row in tags_cursor.fetchall()]
    
    
    rows = []
    if current_tags:
        # Simple query that works on both SQLite and Azure SQL
        placeholders = ','.join('?' * len(current_tags))
        sql = f'''
            SELECT DISTINCT p.id, p.name, p.price, p.original_price, p.thumbnail_url
            FROM products p
            JOIN product_tags pt ON p.id = pt.product_id
            WHERE pt.tag_name IN ({placeholders}) AND p.id != ?
        '''
        params = current_tags + [id]
        
        rec_cursor = db.execute(sql, params)
        rows = rec_cursor.fetchall()
    
    # NEW: Fallback if no tag matches found (or no tags)
    if not rows:
       # No LIMIT here for Azure/T-SQL compatibility
       rec_cursor = db.execute('SELECT * FROM products WHERE id != ?', (id,))
       rows = rec_cursor.fetchall()
    
    # Limit to 5 results
    recs = []
    for row in rows[:5]:
        recs.append({
            'id': row['id'],
            'name': row['name'],
            'price': int(row['price']),
            'original_price': int(row['original_price']) if row['original_price'] else None,
            'thumbnail_url': row['thumbnail_url']
        })
        
    return jsonify(recs)
