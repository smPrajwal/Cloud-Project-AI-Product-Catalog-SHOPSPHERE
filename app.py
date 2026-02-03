import os
from flask import Flask
from flask_cors import CORS
# --- Conditional Loading for Split-Architecture Deployment ---

# 1. Database (Only on Backend)
try:
    from database.db import init_db, close_connection
except ImportError:
    # Frontend instance (No DB access)
    def init_db(app): pass
    def close_connection(e=None): pass

# Loading Routes
# The application is deployed as separate services (Frontend VM / Backend VM).
# We attempt to load whatever modules are available in the artifact.

# 2. Frontend UI
try:
    from frontend_pkg.routes_ui import ui_bp
    app.register_blueprint(ui_bp)
    print("LOG: Loaded UI (Frontend)")
except ImportError:
    pass # Frontend module not present (Backend Server)

# 3. Backend API & Admin
try:
    from backend_pkg.routes_api import api_bp
    from backend_pkg.routes_admin import admin_bp
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
