import os
from flask import g
import time


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        # 1. Try Azure SQL (Required)
        if os.environ.get('AZURE_SQL_CONN'):
            import pyodbc
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
                                    id_cursor = self.conn.cursor()
                                    id_cursor.execute("SELECT @@IDENTITY AS id")
                                    row = id_cursor.fetchone()
                                    if row and row[0]: wrapper.lastrowid = int(row[0])
                                    id_cursor.close()
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

            print("ERROR: Could not connect to Azure SQL after 3 tries.")
            # No fallback, return None or raise error
            raise Exception("Failed to connect to Azure SQL Database.")

        else:
             print("ERROR: AZURE_SQL_CONN environment variable not set.")
             raise Exception("AZURE_SQL_CONN environment variable not set.")
            
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()

        # --- Azure SQL (T-SQL) Initialization ---
        # --- Azure SQL (T-SQL) Initialization ---
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

        # --- Automated Seeding (Integrated) ---
        # --- Automated Seeding (Integrated) ---
        from database.seed_data import seed_azure
        # Pass the raw pyodbc connection
        seed_azure(db.conn)

        # Shared: Data seeding
        
        # Default Footer
        footer_defaults = [
            ('footer_brand_description', 'Your destination for quality products that blend aesthetics with functionality.'),
            ('footer_email', 'prajwalprajwal1999@gmail.com'),
            ('footer_phone', '+91 9035147223')
        ]
        for key, value in footer_defaults:
             # Simple T-SQL check
             exists = db.execute("SELECT 1 FROM site_settings WHERE [key] = ?", (key,)).fetchone()
             if not exists:
                 db.execute("INSERT INTO site_settings ([key], value) VALUES (?, ?)", (key, value))

        # Default Ads
        ads_check = db.execute('SELECT id FROM advertisements').fetchone()
        print(f"LOG: Ads check result: {ads_check}")
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
                db.execute('INSERT INTO advertisements (badge, title, subtitle, button_text, category, image_url, gradient) VALUES (?, ?, ?, ?, ?, ?, ?)', ad)
            db.commit()
            print(f"LOG: Inserted {len(default_ads)} ads")
        else:
            print("LOG: Ads already exist, skipping seed")
