from flask import Blueprint, render_template, request, session, redirect, url_for
import os

ui_bp = Blueprint('ui', __name__, template_folder='templates', static_folder='static')

def safe_get_ads():
    import requests
    backend_url = os.environ.get('BACKEND_API_URL')
    if not backend_url:
        print("ERROR: BACKEND_API_URL not set")
        return []
    try:
        resp = requests.get(f'{backend_url}/api/ads', timeout=5)
        if resp.ok:
            ads = resp.json()
            return ads
    except Exception as e:
        print(f"LOG: safe_get_ads error: {e}") # Keeping error log as it is important
    return []

def safe_get_footer():
    return {'email': 'prajwalprajwal1999@gmail.com', 'phone': '+91 9035147223'}

def safe_get_about():
    return {
        'about_title': 'Our Story',
        'about_subtitle': 'Passionate about quality. Dedicated to you.',
        'about_hero_image': '/static/uploads/about_hero_about_hero.png',
        'about_section1_title': 'How We Started',
        'about_section1_text': 'We are obsessive about curating the finest selection of products that blend premium quality with thoughtful design. Every item in our catalog is chosen with care to enhance your everyday life.',
        'about_section2_title': 'Our Passion',
        'about_section2_text': 'We believe that great design should be accessible to everyone. Our mission is to bring you beautiful, functional products without the luxury markup.'
    }

@ui_bp.route('/api/<path:path>', methods=['GET', 'POST', 'DELETE'])
def proxy(path):
    import requests
    backend_url = os.environ.get('BACKEND_API_URL')
    if not backend_url:
        print("ERROR: BACKEND_API_URL not set")
        return []
    headers = {}
    if session.get('is_admin'):
        headers['X-Admin'] = 'true'
    
    # Handle file uploads
    if request.files:
        files = {k: (f.filename, f.read(), f.content_type) for k, f in request.files.items()}
        resp = requests.request(method=request.method, url=f"{backend_url}/api/{path}", params=request.args, files=files, headers=headers)
    else:
        resp = requests.request(method=request.method, url=f"{backend_url}/api/{path}", params=request.args, json=request.get_json(silent=True), headers=headers)
    return resp.content, resp.status_code

@ui_bp.route('/')
def index():
    return render_template('pages/index.html', ads=safe_get_ads(), footer=safe_get_footer())

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
    return render_template('pages/about.html', content=safe_get_about(), footer=safe_get_footer())

@ui_bp.route('/product/<slug>')
def product_detail(slug):
    return render_template('pages/product.html', product_id=slug, footer=safe_get_footer())
