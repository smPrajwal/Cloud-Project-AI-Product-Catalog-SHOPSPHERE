from flask import Blueprint, request, jsonify, session
from database.db import get_db, query_db, query_one, execute_db, insert_get_id
from common.utils import analyze_sentiment


api_bp = Blueprint('api', __name__)

# --- Products API ---

@api_bp.route('/api/products', methods=['GET'])
def get_products():
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
        
    sql += " ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([offset, limit])
    
    rows = query_db(sql, params)
    
    products = []
    if rows:
        ids = [row['id'] for row in rows]
        placeholders = ','.join('?' * len(ids))
        tags_query = f"SELECT product_id, tag_name FROM product_tags WHERE product_id IN ({placeholders})"
        t_rows = query_db(tags_query, ids)
        
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
    # Handle Slug vs ID
    product = None
    if str(id_or_slug).isdigit():
        product = query_one('SELECT * FROM products WHERE id = ?', (id_or_slug,))
    else:
        # Slug search
        search = '%' + '%'.join(id_or_slug.split('-')) + '%'
        product = query_one('SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,))
    
    if not product:
        return jsonify({'error': 'Not found'}), 404
        
    id = product['id'] # Resolved ID
    
    t_rows = query_db('SELECT tag_name FROM product_tags WHERE product_id = ?', (id,))
    tags = [row['tag_name'] for row in t_rows]
    
    reviews = query_db('SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC', (id,))
    
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
    # Resolve ID
    if str(id_or_slug).isdigit():
        id = id_or_slug
    else:
        search = '%' + '%'.join(id_or_slug.split('-')) + '%'
        row = query_one('SELECT id FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,))
        if not row: return jsonify({'error': 'Product not found'}), 404
        id = row['id']

    data = request.json
    reviewer = data.get('reviewer', '')
    text = data.get('review_text', '')
    
    if not reviewer or not text:
        return jsonify({'error': 'Missing data'}), 400

    sentiment = analyze_sentiment(text)
    
    # Insert and get ID atomically
    review_id = insert_get_id('''
        INSERT INTO reviews (product_id, reviewer, review_text, sentiment_score, sentiment_label) 
        VALUES (?, ?, ?, ?, ?);
        SELECT SCOPE_IDENTITY();
    ''', (id, reviewer, text, sentiment['score'], sentiment['label']))
    
    return jsonify({'message': 'Review added', 'sentiment': sentiment, 'id': review_id})

@api_bp.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    if not session.get('is_admin') and request.headers.get('X-Admin') != 'true':
         return jsonify({'error': 'Admins only'}), 403
         
    execute_db('DELETE FROM reviews WHERE id = ?', (id,))
    
    return jsonify({'message': 'Review deleted'})

@api_bp.route('/api/ads', methods=['GET'])
def get_ads():
    return jsonify(query_db('SELECT * FROM advertisements'))

@api_bp.route('/api/products/<id_or_slug>/recommendations', methods=['GET'])
def get_recommendations(id_or_slug):
    try:
        # Resolve ID if slug is passed
        product_id = None
        if str(id_or_slug).isdigit():
            product_id = int(id_or_slug)
        else:
            search = '%' + '%'.join(id_or_slug.split('-')) + '%'
            p_row = query_one('SELECT id FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,))
            if not p_row:
                return jsonify([])
            product_id = p_row['id']

        
        t_rows = query_db('SELECT tag_name FROM product_tags WHERE product_id = ?', (product_id,))
        current_tags = [row['tag_name'] for row in t_rows]
        
        if not current_tags:
            return jsonify([])
        
        # Simple query for recommendations
        placeholders = ','.join('?' * len(current_tags))
        sql = f'''
            SELECT DISTINCT p.id, p.name, p.price, p.original_price, p.thumbnail_url
            FROM products p
            JOIN product_tags pt ON p.id = pt.product_id
            WHERE pt.tag_name IN ({placeholders}) AND p.id != ?
        '''
        params = current_tags + [product_id]
        
        rows = query_db(sql, params)
        print(f"LOG: Found {len(rows)} recommendation rows")
        
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
    except Exception as e:
        print(f"ERROR in recommendations: {e}")
        return jsonify([])
