import pyodbc, os
from flask import g

# 1. Connect to Azure SQL
def get_db():
    if not hasattr(g, 'db'):
        conn_str = os.environ.get('AZURE_SQL_CONN')
        if not conn_str: return None
        try:
            g.db = pyodbc.connect(conn_str, timeout=10)
        except: return None
    return g.db

def close_connection(e):
    if hasattr(g, 'db'): g.db.close()

# 2. Simple Helpers
def execute_db(sql, params=()):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    return cursor

def query_db(sql, params=()):
    cursor = execute_db(sql, params)
    return [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]

def query_one(sql, params=()):
    rows = query_db(sql, params)
    return rows[0] if rows else None

def insert_get_id(sql, params=()):
    cursor = execute_db(sql, params)
    return int(cursor.fetchone()[0]) if cursor.description else None

# 3. Setup Tables & Data
def init_db(app):
    with app.app_context():
        # Create Tables
        tables = [
            "products (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(MAX), description NVARCHAR(MAX), price REAL, original_price REAL, thumbnail_url NVARCHAR(MAX))",
            "reviews (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, reviewer NVARCHAR(MAX), review_text NVARCHAR(MAX), sentiment_score REAL, sentiment_label NVARCHAR(MAX))",
            "product_tags (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, tag_name NVARCHAR(MAX))",
            "site_settings ([key] NVARCHAR(450) PRIMARY KEY, value NVARCHAR(MAX))",
            "advertisements (id INT IDENTITY(1,1) PRIMARY KEY, badge NVARCHAR(MAX), title NVARCHAR(MAX), subtitle NVARCHAR(MAX), button_text NVARCHAR(MAX), category NVARCHAR(MAX), image_url NVARCHAR(MAX), gradient NVARCHAR(MAX))"
        ]
        for t in tables:
            name = t.split(' ')[0]
            execute_db(f"IF OBJECT_ID('{name}', 'U') IS NULL CREATE TABLE {t}")

        # Seed Products/Reviews
        from database.seed_data import seed_azure
        seed_azure(get_db())

        # Seed Ads (Only if missing)
        ads = [
            ('LIMITED TIME', 'Tech Fest Sale', 'Up to 40% off', 'Shop Now', 'tech', '/static/uploads/promo_electronics.png', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
            ('NEW ARRIVALS', 'Fashion Week', 'Trendy styles', 'Explore', 'fashion', '/static/uploads/promo_fashion.png', 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'),
            ('MEGA SALE', 'Kitchen Essentials', 'Premium appliances', 'Shop Now', 'kitchen', '/static/uploads/promo_kitchen.png', 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'),
            ('TRENDING', 'Lifestyle Picks', 'Curated for you', 'Discover', 'lifestyle', '/static/uploads/promo_lifestyle.png', 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'),
            ('WORK SMART', 'Office Essentials', 'Upgrade workspace', 'Shop Now', 'office', '/static/uploads/promo_office.png', 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)')
        ]
        for ad in ads:
            if not query_one("SELECT 1 FROM advertisements WHERE title = ?", (ad[1],)):
                execute_db("INSERT INTO advertisements (badge, title, subtitle, button_text, category, image_url, gradient) VALUES (?, ?, ?, ?, ?, ?, ?)", ad)

        # Seed Footer (Only if missing)
        settings = [
            ('footer_email', 'prajwalprajwal1999@gmail.com'),
            ('footer_phone', '+91 9035147223')
        ]
        for k, v in settings:
            if not query_one("SELECT 1 FROM site_settings WHERE [key] = ?", (k,)):
                execute_db("INSERT INTO site_settings ([key], value) VALUES (?, ?)", (k, v))
