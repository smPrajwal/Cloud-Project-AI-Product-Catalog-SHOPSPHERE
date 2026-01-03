import os
from flask import Flask
from flask_cors import CORS
from database.db import init_db, close_connection
from shared_pkg.utils import format_indian_currency

app = Flask(__name__)
CORS(app) # Allow Frontend to talk to Backend

# Configuration
app.secret_key = os.environ.get('FLASK_SECRET', 'super_secret_key_for_demo')
DB_FILE = 'database/product_catalog.db'

# Register Filters
app.jinja_env.filters['indian_format'] = format_indian_currency

# --- Conditional Loading for Decoupling ---

# 1. Try Loading UI (Frontend)
try:
    from frontend_pkg.routes_ui import ui_bp
    app.register_blueprint(ui_bp)
    print("LOG: Loaded UI (Frontend)")
except ImportError:
    print("LOG: UI Module not found - Running in Headless Mode")
except Exception as e:
    print(f"LOG: UI Load Error: {e}")

# 2. Try Loading API (Backend)
try:
    from backend_pkg.routes_api import api_bp
    app.register_blueprint(api_bp)
    
    # 3. Only Load Admin if API is present (Backend Only)
    from backend_pkg.routes_admin import admin_bp
    app.register_blueprint(admin_bp)
    
    print("LOG: Loaded API & Admin (Backend)")
except ImportError:
    print("LOG: API Module not found - Running in Frontend-Only Mode")
except Exception as e:
    print(f"LOG: API Load Error: {e}")


# Register Teardown
app.teardown_appcontext(close_connection)

# Ensure DB and migrations are applied on every start (idempotent)
try:
    init_db(app)
except Exception:
    print("LOG: DB Init skipped (Likely Frontend Server)")

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
