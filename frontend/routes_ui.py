from flask import Blueprint, render_template, request, session, redirect, url_for
import os, requests

ui_bp = Blueprint('ui', __name__, template_folder='templates', static_folder='static')

# --- Static Data ---
FOOTER = {'email': 'prajwalprajwal1999@gmail.com', 'phone': '+91 9035147223'}

ABOUT_DATA = {
    'about_title': 'Our Story',
    'about_subtitle': 'Passionate about quality. Dedicated to you.',
    'about_hero_image': '/static/uploads/about_hero_about_hero.png',
    'about_section1_title': 'How We Started',
    'about_section1_text': 'We are obsessive about curating the finest selection of products that blend premium quality with thoughtful design. Every item in our catalog is chosen with care to enhance your everyday life.',
    'about_section2_title': 'Our Passion',
    'about_section2_text': 'We believe that great design should be accessible to everyone. Our mission is to bring you beautiful, functional products without the luxury markup.'
}

# --- Helper ---
def get_ads():
    try:
        url = os.environ.get('BACKEND_API_URL')
        return requests.get(f'{url}/api/ads', timeout=3).json() if url else []
    except:
        return []

# --- Pages ---
@ui_bp.route('/')
def index():
    return render_template('pages/index.html', ads=get_ads(), footer=FOOTER)

@ui_bp.route('/about')
def about():
    return render_template('pages/about.html', content=ABOUT_DATA, footer=FOOTER)

@ui_bp.route('/product/<slug>')
def product_detail(slug):
    return render_template('pages/product.html', product_id=slug, footer=FOOTER)

@ui_bp.route('/health')
def health():
    return "OK", 200

# --- Admin & Proxy ---
@ui_bp.route('/admin-auth')
def admin_login():
    auth = request.authorization
    u, p = os.environ.get('ADMIN_USERNAME'), os.environ.get('ADMIN_PASSWORD')
    if auth and auth.username == u and auth.password == p:
        session['is_admin'] = True
        return redirect(url_for('ui.index'))
    return 'Login required', 401, {'WWW-Authenticate': 'Basic realm="Admin"'}

@ui_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('ui.index'))

@ui_bp.route('/api/<path:path>', methods=['GET', 'POST', 'DELETE'])
def api_proxy(path):
    url = f"{os.environ.get('BACKEND_API_URL')}/api/{path}"
    headers = {'X-Admin': 'true'} if session.get('is_admin') else {}
    
    # Forward Files or JSON
    if request.files:
        files = {k: (f.filename, f.read(), f.content_type) for k, f in request.files.items()}
        resp = requests.request(request.method, url, params=request.args, files=files, headers=headers)
    else:
        resp = requests.request(request.method, url, params=request.args, json=request.get_json(silent=True), headers=headers)
        
    return resp.content, resp.status_code
