import sqlite3
import os
from flask import g
import time
import pyodbc

DB_FILE = 'database/product_catalog.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # 1. Try Azure SQL (if env var exists)
        if os.environ.get('AZURE_SQL_CONN'):
            # Retry loop for Azure Free Tier (It sleeps when idle)
            for attempt in range(3):
                try:
                    conn_str = os.environ.get('AZURE_SQL_CONN')
                    conn = pyodbc.connect(conn_str, timeout=10)
                    
                    # --- AzureDB Wrapper Class (Same as before) ---
                    class AzureDB:
                        def __init__(self, conn): self.conn = conn
                        def execute(self, sql, params=()):
                            c = self.conn.cursor()
                            c.execute(sql, params)
                            wrapper = AzureCursor(c)
                            if sql.strip().upper().startswith("INSERT"):
                                try:
                                    c.execute("SELECT CAST(SCOPE_IDENTITY() AS INT)")
                                    row = c.fetchone()
                                    if row: wrapper.lastrowid = row[0]
                                except: pass
                            return wrapper
                        def commit(self): self.conn.commit()
                        def close(self): self.conn.close()

                    class AzureCursor:
                        def __init__(self, cursor): 
                            self.cursor = cursor
                            self.lastrowid = None
                        def fetchone(self):
                            row = self.cursor.fetchone()
                            return dict(zip([d[0] for d in self.cursor.description], row)) if row else None
                        def fetchall(self):
                            cols = [d[0] for d in self.cursor.description]
                            return [dict(zip(cols, row)) for row in self.cursor.fetchall()]
                        def close(self): self.cursor.close()

                    # Connection Successful
                    db = g._database = AzureDB(conn)
                    print(f"LOG: Connected to Azure SQL (Attempt {attempt+1})")
                    return db
                    
                except Exception as e:
                    print(f"Azure Connection Failed (Attempt {attempt+1}): {e}")
                    time.sleep(5) # Wait for DB to wake up

            print("ERROR: Could not connect to Azure SQL after 3 tries. Falling back to Local.")

        # 2. SQLite Fallback (Local Mode or Azure Failure)
        if db is None:
            db = g._database = sqlite3.connect(DB_FILE)
            db.row_factory = sqlite3.Row
            
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        if os.environ.get('AZURE_SQL_CONN'):
            # --- Azure SQL (T-SQL) Initialization ---
            try:
                # products
                db.execute("IF OBJECT_ID('products', 'U') IS NULL CREATE TABLE products (id INT IDENTITY(1,1) PRIMARY KEY, name NVARCHAR(MAX) NOT NULL, description NVARCHAR(MAX), price REAL, original_price REAL, thumbnail_url NVARCHAR(MAX))")
                # reviews
                db.execute("IF OBJECT_ID('reviews', 'U') IS NULL CREATE TABLE reviews (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, reviewer NVARCHAR(MAX), review_text NVARCHAR(MAX), sentiment_score REAL, sentiment_label NVARCHAR(MAX), FOREIGN KEY(product_id) REFERENCES products(id))")
                # product_tags
                db.execute("IF OBJECT_ID('product_tags', 'U') IS NULL CREATE TABLE product_tags (id INT IDENTITY(1,1) PRIMARY KEY, product_id INT, tag_name NVARCHAR(MAX), FOREIGN KEY(product_id) REFERENCES products(id))")
                # site_settings
                db.execute("IF OBJECT_ID('site_settings', 'U') IS NULL CREATE TABLE site_settings ([key] NVARCHAR(450) PRIMARY KEY, value NVARCHAR(MAX))")
                # advertisements
                db.execute("IF OBJECT_ID('advertisements', 'U') IS NULL CREATE TABLE advertisements (id INT IDENTITY(1,1) PRIMARY KEY, badge NVARCHAR(MAX), title NVARCHAR(MAX), subtitle NVARCHAR(MAX), button_text NVARCHAR(MAX), category NVARCHAR(MAX), image_url NVARCHAR(MAX), gradient NVARCHAR(MAX))")
            except Exception as e:
                print(f"Azure DB Init Error (ignoring if tables exist): {e}")

        else:
            # --- SQLite Initialization ---
            # Products table
            db.execute('''CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                original_price REAL,
                thumbnail_url TEXT
            )''')
            # Reviews table
            db.execute('''CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                reviewer TEXT,
                review_text TEXT,
                sentiment_score REAL,
                sentiment_label TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )''')
            # ProductTags table
            db.execute('''CREATE TABLE IF NOT EXISTS product_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER,
                tag_name TEXT,
                FOREIGN KEY(product_id) REFERENCES products(id)
            )''')
            # Site settings
            db.execute('''CREATE TABLE IF NOT EXISTS site_settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )''')
            # Advertisements
            db.execute('''CREATE TABLE IF NOT EXISTS advertisements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                badge TEXT,
                title TEXT,
                subtitle TEXT,
                button_text TEXT,
                category TEXT,
                image_url TEXT,
                gradient TEXT
            )''')
            
            # Optimize Indexes (SQLite only)
            db.execute('CREATE INDEX IF NOT EXISTS idx_products_name ON products(name)')
            db.execute('CREATE INDEX IF NOT EXISTS idx_tags_tagname ON product_tags(tag_name)')
            db.execute('CREATE INDEX IF NOT EXISTS idx_tags_productid ON product_tags(product_id)')

        # Shared: Data seeding (Safe for both)
        
        # Default Footer
        footer_defaults = [
            ('footer_brand_description', 'Your destination for quality products that blend aesthetics with functionality.'),
            ('footer_email', 'prajwalprajwal1999@gmail.com'),
            ('footer_phone', '+91 9035147223')
        ]
        for key, value in footer_defaults:
            # T-SQL uses MERGE or IF EXISTS, but simple INSERT OR IGNORE is SQLite specific.
            # Universal way: Check then insert.
            if os.environ.get('AZURE_SQL_CONN'):
                 # Simple T-SQL check
                 exists = db.execute("SELECT 1 FROM site_settings WHERE [key] = ?", (key,)).fetchone()
                 if not exists:
                     db.execute("INSERT INTO site_settings ([key], value) VALUES (?, ?)", (key, value))
            else:
                 db.execute('INSERT OR IGNORE INTO site_settings (key, value) VALUES (?, ?)', (key, value))

        # Default Ads (Same logic)
        
        ads_check = db.execute('SELECT id FROM advertisements').fetchone()
        if not ads_check:
             default_ads = [
                ('LIMITED TIME', 'Tech Fest Sale', 'Up to 40% off on Electronics', 'Shop Now →', 'tech', '/static/uploads/promo_electronics.png', 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'),
                ('NEW ARRIVALS', 'Fashion Week', 'Trendy styles at best prices', 'Explore →', 'fashion', '/static/uploads/promo_fashion.png', 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'),
                ('MEGA SALE', 'Kitchen Essentials', 'Premium appliances at 30% off', 'Shop Now →', 'kitchen', '/static/uploads/promo_kitchen.png', 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'),
                ('TRENDING', 'Lifestyle Picks', 'Curated collection for you', 'Discover →', 'lifestyle', '/static/uploads/promo_lifestyle.png', 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)')
            ]
             for ad in default_ads:
                db.execute('INSERT INTO advertisements (badge, title, subtitle, button_text, category, image_url, gradient) VALUES (?, ?, ?, ?, ?, ?, ?)', ad)
        

        
