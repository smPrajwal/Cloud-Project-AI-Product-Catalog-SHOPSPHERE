from flask import Blueprint, render_template, request, session, redirect, url_for
import os

ui_bp = Blueprint('ui', __name__)

def safe_get_ads():
    import requests
    backend_url = os.environ.get('BACKEND_API_URL', 'http://localhost:5000')
    try:
        resp = requests.get(f"{backend_url}/api/ads", timeout=5)
        if resp.ok:
            return resp.json()
    except:
        pass
    return []

def safe_get_footer():
    return {'email': 'prajwalprajwal1999@gmail.com', 'phone': '+91 9035147223'}

def safe_get_about():
    return {
        'about_title': 'Our Story',
        'about_subtitle': 'Passionate about quality. Dedicated to you.',
        'about_hero_image': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=800',
        'about_section1_title': 'How We Started',
        'about_section1_text': 'ShopSphere began with a simple idea: make quality products accessible to everyone. What started as a small online store has grown into a trusted destination for shoppers looking for the best deals on electronics, fashion, home goods, and more.',
        'about_section2_title': 'Our Passion',
        'about_section2_text': 'We believe shopping should be simple, enjoyable, and rewarding. Our team works hard to bring you carefully selected products at the best prices. Customer satisfaction is at the heart of everything we do.'
    }

@ui_bp.route('/api/<path:path>', methods=['GET', 'POST', 'DELETE'])
def proxy(path):
    import requests
    backend_url = os.environ.get('BACKEND_API_URL', 'http://localhost:8000')
    resp = requests.request(method=request.method, url=f"{backend_url}/api/{path}", params=request.args, json=request.get_json(silent=True))
    return resp.content, resp.status_code

@ui_bp.route('/')
def index():
    return render_template('index.html', ads=safe_get_ads(), footer=safe_get_footer())

@ui_bp.route('/health')
def health_check():
    return "OK", 200

@ui_bp.route('/admin-auth')
def admin_auth():
    auth = request.authorization
    if not auth: return 'Login required', 401, {'WWW-Authenticate': 'Basic realm="Admin"'}
    u = os.environ.get('ADMIN_USERNAME', '').strip()
    p = os.environ.get('ADMIN_PASSWORD', '').strip()
    if auth.username == u and auth.password == p:
        session['is_admin'] = True
        return redirect(url_for('ui.index'))
    return 'Invalid credentials', 401

@ui_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('ui.index'))

@ui_bp.route('/about')
def about():
    return render_template('about.html', content=safe_get_about(), footer=safe_get_footer())

@ui_bp.route('/product/<slug>')
def product_detail(slug):
    return render_template('product.html', product_id=slug, footer=safe_get_footer())
