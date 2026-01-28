from flask import Blueprint, render_template, request, session, redirect, url_for
import os

ui_bp = Blueprint('ui', __name__)

# --- Safe Helpers (Frontend Friendly) ---
import requests

def safe_get_ads():
    try:
        backend_url = os.environ.get('BACKEND_API_URL', 'http://localhost:8000')
        resp = requests.get(f"{backend_url}/api/advertisements", timeout=2)
        if resp.ok: return resp.json()
    except:
        pass
    return []

def safe_get_footer():
    try:
        backend_url = os.environ.get('BACKEND_API_URL', 'http://localhost:8000')
        resp = requests.get(f"{backend_url}/api/settings/footer", timeout=2)
        if resp.ok: return resp.json()
    except:
        pass
    return {}

def safe_get_about():
    try:
        backend_url = os.environ.get('BACKEND_API_URL', 'http://localhost:8000')
        resp = requests.get(f"{backend_url}/api/settings/about", timeout=2)
        if resp.ok: return resp.json()
    except:
        pass
    return {}

# --- Routes ---

@ui_bp.route('/api/<path:path>', methods=['GET', 'POST', 'DELETE'])
def proxy(path):
    import requests
    backend_url = os.environ.get('BACKEND_API_URL', 'http://localhost:8000')
    url = f"{backend_url}/api/{path}"
    
    # Forward the request
    resp = requests.request(
        method=request.method,
        url=url,
        json=request.get_json(silent=True)
    )
    return resp.content, resp.status_code

@ui_bp.route('/')
def index():
    print("LOG: Accessing index page (UI)")
    return render_template('index.html', ads=safe_get_ads(), footer=safe_get_footer())

@ui_bp.route('/health')
def health_check():
    return "OK", 200

@ui_bp.route('/admin-auth')
def admin_auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return 'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}
    
    required_user = os.environ.get('ADMIN_USERNAME')
    required_pass = os.environ.get('ADMIN_PASSWORD')
    
    if required_user: required_user = required_user.strip()
    if required_pass: required_pass = required_pass.strip()
    
    if not required_user or not required_pass:
        return 'Admin credentials not configured', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}

    if auth.username == required_user and auth.password == required_pass:
        session['user_id'] = 'admin'
        session['username'] = 'admin'
        session['is_admin'] = True
        return redirect(url_for('ui.index'))
    
    return 'Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Admin Login"'}

@ui_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('ui.index'))

@ui_bp.route('/about')
def about():
    return render_template('about.html', content=safe_get_about(), footer=safe_get_footer())

@ui_bp.route('/product/<slug>')
def product_detail(slug):
    # Pass the slug directly to the template. 
    # The Frontend JS will hit the API to resolve it.
    return render_template('product.html', product_id=slug, footer=safe_get_footer())
