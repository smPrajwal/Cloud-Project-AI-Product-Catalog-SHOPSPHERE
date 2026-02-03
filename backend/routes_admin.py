from flask import Blueprint, request, jsonify, session
import time
from database.db import get_db, query_one, execute_db, insert_get_id
from common.utils import upload_product_image

admin_bp = Blueprint('admin', __name__)

# --- Product Admin ---
@admin_bp.route('/api/products', methods=['POST'])
def add_product():
    if not session.get('is_admin') and request.headers.get('X-Admin') != 'true':
         return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    data = request.json
    
    product_id = insert_get_id('INSERT INTO products (name, description, price, original_price, thumbnail_url) VALUES (?, ?, ?, ?, ?); SELECT SCOPE_IDENTITY()',
               (data['name'], data.get('description', ''), data['price'], data.get('original_price'), '/static/uploads/placeholder.png'))
    
    if 'tags' in data and data['tags']:
        for tag in data['tags']:
            execute_db('INSERT INTO product_tags (product_id, tag_name) VALUES (?, ?)', (product_id, tag))
            
    return jsonify({'success': True, 'data': {'id': product_id}, 'message': 'Product created'}), 201

@admin_bp.route('/api/products/<id_or_slug>/image', methods=['POST'])
def add_product_image(id_or_slug):
    if not session.get('is_admin') and request.headers.get('X-Admin') != 'true':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    # Resolve ID
    if str(id_or_slug).isdigit():
        id = id_or_slug
    else:
        search = '%' + '%'.join(id_or_slug.split('-')) + '%'
        row = query_one('SELECT id FROM products WHERE LOWER(name) LIKE LOWER(?)', (search,))
        if not row: return jsonify({'success': False, 'error': 'Product not found'}), 404
        id = row['id']

    file = request.files.get('file')
    if not file:
        return jsonify({'success': False, 'error': 'No file provided'}), 400

    product = query_one('SELECT * FROM products WHERE id = ?', (id,))
    if not product:
        return jsonify({'success': False, 'error': 'Product not found'}), 404

    timestamp = int(time.time())
    
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    # Simple slug (Kid-friendly: just replace spaces)
    safe_name = product['name'].lower().replace(' ', '-')
    
    # Overwrite existing file (Name stays same)
    url, blob_name = upload_product_image(file, safe_name)
    
    if not url:
         return jsonify({'success': False, 'error': 'Failed to save image'}), 500

    # Add timestamp to URL so browser reloads it
    separator = '&' if '?' in url else '?'
    final_url = f"{url}{separator}v={timestamp}"
    
    # Update DB with new "versioned" URL
    execute_db('UPDATE products SET thumbnail_url = ? WHERE id = ?', (final_url, id))
    
    # Clear existing tags so AI can regenerate them for the new image
    execute_db('DELETE FROM product_tags WHERE product_id = ?', (id,))

    return jsonify({'success': True, 'data': {'url': final_url}, 'message': 'Image updated'})

@admin_bp.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    if not session.get('is_admin') and request.headers.get('X-Admin') != 'true':
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    if not query_one('SELECT id FROM products WHERE id = ?', (id,)):
        return jsonify({'success': False, 'error': 'Not found'}), 404
        
    execute_db('DELETE FROM product_tags WHERE product_id = ?', (id,))
    execute_db('DELETE FROM reviews WHERE product_id = ?', (id,))
    execute_db('DELETE FROM products WHERE id = ?', (id,))
    
    return jsonify({'success': True, 'message': 'Product deleted'})
