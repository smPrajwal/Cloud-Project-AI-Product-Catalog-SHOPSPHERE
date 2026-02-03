import os
from flask import Flask
from flask_cors import CORS
from common.utils import format_indian_currency

app = Flask(__name__, static_folder='frontend/static', template_folder='frontend/templates')
CORS(app) # Allow Frontend to talk to Backend

# Configuration
app.secret_key = os.environ.get('FLASK_SECRET', 'super_secret_key_for_demo')

# Register Filters
app.jinja_env.filters['indian_format'] = format_indian_currency

# --- Conditional Loading for Split-Architecture Deployment ---

# 1. Database (Only on Backend)
try:
    from database.db import init_db, close_connection
except ImportError:
    # Frontend instance (No DB access)
    def init_db(app): pass
    def close_connection(e=None): pass

# --- Conditional Loading for Split-Architecture Deployment ---



# Loading Routes
# The application is deployed as separate services (Frontend VM / Backend VM).
# We attempt to load whatever modules are available in the artifact.

# 2. Frontend UI
try:
    from frontend.routes_ui import ui_bp
    app.register_blueprint(ui_bp)
    print("LOG: Loaded UI (Frontend)")
except ImportError:
    pass # Frontend module not present (Backend Server)

# 3. Backend API & Admin
try:
    from backend.routes_api import api_bp
    from backend.routes_admin import admin_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(admin_bp)
    print("LOG: Loaded API & Admin (Backend)")
except ImportError:
    pass # Backend modules not present (Frontend Server)


# Register Teardown
app.teardown_appcontext(close_connection)

# Ensure DB and migrations are applied on every start (idempotent)
try:
    init_db(app)
except Exception as e:
    print(f"LOG: DB Init Warning: {e}")
