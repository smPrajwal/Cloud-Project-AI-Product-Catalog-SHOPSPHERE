import os, time, pyodbc
from flask import g
from database.seed_data import seed_azure

# 1. Connect to Database (Simple & Direct)
def get_db():
    if not getattr(g, '_database', None):
        conn_str = os.environ.get('AZURE_SQL_CONN')
        if not conn_str: return None # No DB configured
        
        # Try connecting (Retry once if needed)
        try:
            g._database = pyodbc.connect(conn_str, timeout=10)
            print("LOG: Connected to Azure SQL")
        except:
            time.sleep(3)
            g._database = pyodbc.connect(conn_str, timeout=10)
            
    return g._database

def close_connection(e):
    db = getattr(g, '_database', None)
    if db: db.close()

# 2. Easy Helpers (Run SQL commands easily)
def query_db(sql, params=()):
    cursor = get_db().cursor()
    cursor.execute(sql, params)
    return [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()] if cursor.description else None

def query_one(sql, params=()):
    res = query_db(sql, params)
    return res[0] if res else None

def execute_db(sql, params=()):
    cursor = get_db().cursor()
    cursor.execute(sql, params)
    get_db().commit()
    return cursor

def insert_get_id(sql, params=()):
    # IMPORTANT: Fetch ID *before* commit to keep SCOPE_IDENTITY() valid
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    
    id = None
    if cursor.nextset(): 
        row = cursor.fetchone()
        if row: id = int(row[0])
            
    conn.commit() # Commit AFTER catching the result
    return id

# 3. Setup Tables & Default Data
def init_db(app):
    with app.app_context():
        if not get_db(): return

        # Create Tables (if they don't exist)
        tables = [
            "products (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(MAX), description NVARCHAR(MAX), price REAL, original_price REAL, thumbnail_url NVARCHAR(MAX))",
            "reviews (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, reviewer NVARCHAR(MAX), review_text NVARCHAR(MAX), sentiment_score REAL, sentiment_label NVARCHAR(MAX), FOREIGN KEY(product_id) REFERENCES products(id))",
            "product_tags (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, tag_name NVARCHAR(MAX), FOREIGN KEY(product_id) REFERENCES products(id))",
            "site_settings ([key] NVARCHAR(450) PRIMARY KEY, value NVARCHAR(MAX))",
            "advertisements (id INT IDENTITY(1,1) PRIMARY KEY, badge NVARCHAR(MAX), title NVARCHAR(MAX), subtitle NVARCHAR(MAX), button_text NVARCHAR(MAX), category NVARCHAR(MAX), image_url NVARCHAR(MAX), gradient NVARCHAR(MAX))"
        ]
        for t in tables:
            name = t.split(' ')[0]
            execute_db(f"IF OBJECT_ID('{name}', 'U') IS NULL CREATE TABLE {t}")

        # Seed Products/Reviews
        seed_azure(get_db())

        # Seed Footer Defaults
        defaults = [
            ('footer_brand_description', 'Your destination for quality products that blend aesthetics with functionality.'),
            ('footer_email', 'prajwalprajwal1999@gmail.com'),
            ('footer_phone', '+91 9035147223')
        ]
        for k, v in defaults:
            if not query_one("SELECT 1 FROM site_settings WHERE [key] = ?", (k,)):
                execute_db("INSERT INTO site_settings ([key], value) VALUES (?, ?)", (k, v))

        # Seed Ads (Single atomic SQL prevents duplicates even with multiple VMSS instances)
        ads = [
            ('LIMITED TIME', 'Tech Fest Sale', 'Up to 40% off on Electronics', 'Shop Now →', 'tech', '/static/uploads/promo_electronics.png', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
            ('NEW ARRIVALS', 'Fashion Week', 'Trendy styles at best prices', 'Explore →', 'fashion', '/static/uploads/promo_fashion.png', 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'),
            ('MEGA SALE', 'Kitchen Essentials', 'Premium appliances at 30% off', 'Shop Now →', 'kitchen', '/static/uploads/promo_kitchen.png', 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'),
            ('TRENDING', 'Lifestyle Picks', 'Curated collection for you', 'Discover →', 'lifestyle', '/static/uploads/promo_lifestyle.png', 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'),
            ('WORK SMART', 'Office Essentials', 'Upgrade your workspace today', 'Shop Now →', 'office', '/static/uploads/promo_office.png', 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)')
        ]
        for ad in ads:
            execute_db("""
                IF NOT EXISTS (SELECT 1 FROM advertisements WHERE title = ?)
                INSERT INTO advertisements (badge, title, subtitle, button_text, category, image_url, gradient)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (ad[1], *ad))
