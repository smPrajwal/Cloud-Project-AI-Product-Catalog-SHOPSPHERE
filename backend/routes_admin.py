from flask import Blueprint, request, jsonify, session
import time
from database.db import query_one, execute_db, insert_get_id
from common.utils import upload_product_image

admin_bp = Blueprint('admin', __name__)

# Authentication Helper
def is_admin():
    return session.get('is_admin') or request.headers.get('X-Admin') == 'true'

@admin_bp.route('/api/products', methods=['POST'])
def add_product():
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.json
    
    # Add Product
    sql = "INSERT INTO products (name, description, price, original_price, thumbnail_url) VALUES (?, ?, ?, ?, ?); SELECT SCOPE_IDENTITY()"
    pid = insert_get_id(sql, (data['name'], data.get('description', ''), data['price'], data.get('original_price'), '/static/uploads/placeholder.png'))
    
    # Add Tags
    for tag in data.get('tags', []):
        execute_db("INSERT INTO product_tags (product_id, tag_name) VALUES (?, ?)", (pid, tag))
            
    return jsonify({'success': True, 'data': {'id': pid}, 'message': 'Product created'}), 201

@admin_bp.route('/api/products/<id_or_slug>/image', methods=['POST'])
def add_product_image(id_or_slug):
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 401

    # 1. Get Product ID
    if id_or_slug.isdigit():
        pid = id_or_slug
    else:
        # Find ID by name (e.g. "Wireless-Headphones" -> "Wireless Headphones")
        name = id_or_slug.replace('-', ' ') 
        row = query_one("SELECT id, name FROM products WHERE name LIKE ?", ('%' + name + '%',))
        if not row: return jsonify({'error': 'Product not found'}), 404
        pid = row['id']

    # 2. Upload File
    file = request.files.get('file')
    if not file: return jsonify({'error': 'No file'}), 400
    
    # Get Name for File
    product = query_one("SELECT name FROM products WHERE id = ?", (pid,))
    safe_name = product['name'].lower().replace(' ', '-')

    # Upload to Cloud
    url, _ = upload_product_image(file, safe_name)
    if not url: return jsonify({'error': 'Upload failed'}), 500

    # 3. Update Database (Add timestamp to URL to force refresh)
    final_url = f"{url}?v={int(time.time())}"
    execute_db("UPDATE products SET thumbnail_url = ? WHERE id = ?", (final_url, pid))
    
    # Clear old tags so they can be regenerated
    execute_db("DELETE FROM product_tags WHERE product_id = ?", (pid,))

    return jsonify({'success': True, 'data': {'url': final_url}, 'message': 'Image updated'})

@admin_bp.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    if not is_admin(): return jsonify({'error': 'Unauthorized'}), 401
    
    # Delete everything related to the product
    execute_db("DELETE FROM product_tags WHERE product_id = ?", (id,))
    execute_db("DELETE FROM reviews WHERE product_id = ?", (id,))
    execute_db("DELETE FROM products WHERE id = ?", (id,))
    
    return jsonify({'success': True, 'message': 'Product deleted'})
