from flask import Blueprint, request, jsonify, session
from database.db import query_db, query_one, execute_db, insert_get_id
from common.utils import analyze_sentiment

api_bp = Blueprint('api', __name__)

# Helper: Find Product ID from Number or Name
def resolve_id(id_or_slug):
    if str(id_or_slug).isdigit():
        return int(id_or_slug)
    # Search by name (e.g. "blue-shirt" -> "blue shirt")
    name_search = id_or_slug.replace('-', ' ')
    row = query_one("SELECT id FROM products WHERE name LIKE ?", ('%' + name_search + '%',))
    return row['id'] if row else None

@api_bp.route('/api/products', methods=['GET'])
def get_products():
    args = request.args
    sql = "SELECT * FROM products WHERE 1=1"
    params = []

    # 1. Search Filter
    if args.get('q'):
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{args.get('q')}%", f"%{args.get('q')}%"])
    
    # 2. Tag Filter
    if args.get('tag'):
        sql += " AND id IN (SELECT product_id FROM product_tags WHERE tag_name = ?)"
        params.append(args.get('tag'))

    # 3. Paging
    sql += " ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
    params.extend([args.get('offset', 0), args.get('limit', 100)])

    # 4. Fetch Results
    rows = query_db(sql, params)
    
    # 5. Attach Tags to each product
    results = []
    for p in rows:
        tags = [t['tag_name'] for t in query_db("SELECT tag_name FROM product_tags WHERE product_id = ?", (p['id'],))]
        results.append({**p, 'tags': tags, 'price': int(p['price']), 'discount_percent': 0})
        
    return jsonify(results)

@api_bp.route('/api/products/<id_or_slug>', methods=['GET'])
def get_product_details(id_or_slug):
    id = resolve_id(id_or_slug)
    if not id: return jsonify({'error': 'Not found'}), 404

    product = query_one("SELECT * FROM products WHERE id = ?", (id,))
    tags = [row['tag_name'] for row in query_db("SELECT tag_name FROM product_tags WHERE product_id = ?", (id,))]
    reviews = query_db("SELECT * FROM reviews WHERE product_id = ? ORDER BY id DESC", (id,))

    return jsonify({**product, 'tags': tags, 'reviews': reviews, 'price': int(product['price'])})

@api_bp.route('/api/products/<id_or_slug>/reviews', methods=['POST'])
def add_review(id_or_slug):
    id = resolve_id(id_or_slug)
    if not id: return jsonify({'error': 'Not found'}), 404

    data = request.json
    sentiment = analyze_sentiment(data['review_text'])

    sql = "INSERT INTO reviews (product_id, reviewer, review_text, sentiment_score, sentiment_label) VALUES (?, ?, ?, ?, ?); SELECT SCOPE_IDENTITY()"
    rid = insert_get_id(sql, (id, data['reviewer'], data['review_text'], sentiment['score'], sentiment['label']))
    
    return jsonify({'message': 'Review added', 'sentiment': sentiment, 'id': rid})

@api_bp.route('/api/reviews/<int:id>', methods=['DELETE'])
def delete_review(id):
    # Check Admin
    if not session.get('is_admin') and request.headers.get('X-Admin') != 'true':
        return jsonify({'error': 'Admins only'}), 403
        
    execute_db('DELETE FROM reviews WHERE id = ?', (id,))
    return jsonify({'message': 'Review deleted'})

@api_bp.route('/api/ads', methods=['GET'])
def get_ads():
    return jsonify(query_db('SELECT * FROM advertisements'))

@api_bp.route('/api/products/<id_or_slug>/recommendations', methods=['GET'])
def get_recommendations(id_or_slug):
    id = resolve_id(id_or_slug)
    if not id: return jsonify([])

    # Find stats with same tags
    sql = """
        SELECT DISTINCT TOP 5 p.* FROM products p
        JOIN product_tags pt ON p.id = pt.product_id
        WHERE pt.tag_name IN (SELECT tag_name FROM product_tags WHERE product_id = ?)
        AND p.id != ?
    """
    rows = query_db(sql, (id, id))
    return jsonify([{**row, 'price': int(row['price'])} for row in rows])
