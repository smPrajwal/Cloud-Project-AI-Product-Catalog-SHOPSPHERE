import os
from flask import g
import time
import pyodbc

def get_db():
    conn = getattr(g, '_database', None)
    if conn is None:
        if not os.environ.get('AZURE_SQL_CONN'):
             print("ERROR: AZURE_SQL_CONN environment variable not set.")
             raise Exception("AZURE_SQL_CONN environment variable not set.")

        conn_str = os.environ.get('AZURE_SQL_CONN')
        
        # Retry loop for connection
        for attempt in range(3):
            try:
                # Direct PyODBC Connection
                conn = pyodbc.connect(conn_str, timeout=10)
                g._database = conn
                print(f"LOG: Connected to Azure SQL (Attempt {attempt+1})")
                return conn
            except Exception as e:
                print(f"Azure Connection Failed (Attempt {attempt+1}): {e}")
                time.sleep(5)
        
        raise Exception("Failed to connect to Azure SQL Database.")

    return conn

def close_connection(exception):
    conn = getattr(g, '_database', None)
    if conn is not None:
        conn.close()

# --- Helpers ---

def query_db(sql, params=()):
    """Returns a list of dictionaries."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    if cursor.description:
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
    return None

def query_one(sql, params=()):
    """Returns a single dictionary or None."""
    rows = query_db(sql, params)
    return rows[0] if rows else None

def execute_db(sql, params=()):
    """Executes a write operation and commits. Returns the cursor."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    return cursor

def insert_get_id(sql, params=()):
    """Executes INSERT ...; SELECT SCOPE_IDENTITY() and returns the ID."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    if cursor.nextset(): 
        row = cursor.fetchone()
        if row:
             id = int(row[0])
             conn.commit()
             return id
    conn.commit()
    return None

# --- Init ---

def init_db(app):
    with app.app_context():
        # Ensure connection logic is sound
        try:
            get_db()
        except:
            return # Skip if no DB configured (e.g. build step)

        # products
        execute_db("IF OBJECT_ID('products', 'U') IS NULL CREATE TABLE products (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(MAX) NOT NULL, description NVARCHAR(MAX), price REAL, original_price REAL, thumbnail_url NVARCHAR(MAX))")
        # reviews
        execute_db("IF OBJECT_ID('reviews', 'U') IS NULL CREATE TABLE reviews (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, reviewer NVARCHAR(MAX), review_text NVARCHAR(MAX), sentiment_score REAL, sentiment_label NVARCHAR(MAX), FOREIGN KEY(product_id) REFERENCES products(id))")
        # product_tags
        execute_db("IF OBJECT_ID('product_tags', 'U') IS NULL CREATE TABLE product_tags (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, tag_name NVARCHAR(MAX), FOREIGN KEY(product_id) REFERENCES products(id))")
        # site_settings
        execute_db("IF OBJECT_ID('site_settings', 'U') IS NULL CREATE TABLE site_settings ([key] NVARCHAR(450) PRIMARY KEY, value NVARCHAR(MAX))")
        # advertisements
        execute_db("IF OBJECT_ID('advertisements', 'U') IS NULL CREATE TABLE advertisements (id INT IDENTITY(1,1) PRIMARY KEY, badge NVARCHAR(MAX), title NVARCHAR(MAX), subtitle NVARCHAR(MAX), button_text NVARCHAR(MAX), category NVARCHAR(MAX), image_url NVARCHAR(MAX), gradient NVARCHAR(MAX))")

        # --- Automated Seeding ---
        from database.seed_data import seed_azure
        seed_azure(get_db())

        # Default Footer
        footer_defaults = [
            ('footer_brand_description', 'Your destination for quality products that blend aesthetics with functionality.'),
            ('footer_email', 'prajwalprajwal1999@gmail.com'),
            ('footer_phone', '+91 9035147223')
        ]
        for key, value in footer_defaults:
             exists = query_one("SELECT 1 FROM site_settings WHERE [key] = ?", (key,))
             if not exists:
                 execute_db("INSERT INTO site_settings ([key], value) VALUES (?, ?)", (key, value))

        # Default Ads
        ads_check = query_one('SELECT id FROM advertisements')
        if not ads_check:
            print("LOG: Seeding advertisements...")
            default_ads = [
                ('LIMITED TIME', 'Tech Fest Sale', 'Up to 40% off on Electronics', 'Shop Now →', 'tech', '/static/uploads/promo_electronics.png', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
                ('NEW ARRIVALS', 'Fashion Week', 'Trendy styles at best prices', 'Explore →', 'fashion', '/static/uploads/promo_fashion.png', 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'),
                ('MEGA SALE', 'Kitchen Essentials', 'Premium appliances at 30% off', 'Shop Now →', 'kitchen', '/static/uploads/promo_kitchen.png', 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'),
                ('TRENDING', 'Lifestyle Picks', 'Curated collection for you', 'Discover →', 'lifestyle', '/static/uploads/promo_lifestyle.png', 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'),
                ('WORK SMART', 'Office Essentials', 'Upgrade your workspace today', 'Shop Now →', 'office', '/static/uploads/promo_office.png', 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)')
            ]
            for ad in default_ads:
                # Check if specific ad exists (logic: title must be unique)
                if not query_one("SELECT 1 FROM advertisements WHERE title = ?", (ad[1],)):
                     execute_db('INSERT INTO advertisements (badge, title, subtitle, button_text, category, image_url, gradient) VALUES (?, ?, ?, ?, ?, ?, ?)', ad)
            print(f"LOG: Seeding check complete for ads")
        else:
            print("LOG: Ads already exist, skipping seed")
