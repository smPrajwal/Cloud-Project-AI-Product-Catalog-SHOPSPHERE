import os
from flask import Flask
from flask_cors import CORS
# Trigger reload
from database.db import init_db, close_connection
from backend.utils import format_indian_currency
from backend.routes_admin import admin_bp
from backend.routes_public import common_bp

app = Flask(__name__)
CORS(app) # Allow Frontend to talk to Backend

# Configuration
app.secret_key = os.environ.get('FLASK_SECRET', 'super_secret_key_for_demo')
DB_FILE = 'database/product_catalog.db'

# Register Filters
app.jinja_env.filters['indian_format'] = format_indian_currency

# Register Blueprints
app.register_blueprint(common_bp)
app.register_blueprint(admin_bp)

# Register Teardown
app.teardown_appcontext(close_connection)

# Ensure DB and migrations are applied on every start (idempotent)
init_db(app)

if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    app.run(host='0.0.0.0', debug=debug_mode, port=5000)
