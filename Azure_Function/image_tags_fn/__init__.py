import os
import pyodbc
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def main(blob):
    # 1. Connect to DB first
    db = pyodbc.connect(os.environ["AZURE_SQL_CONN"])
    cur = db.cursor()

    # 2. Find Product ID
    cur.execute(
        "SELECT id FROM products WHERE thumbnail_url LIKE ?",
        ("%" + blob.name + "%",)
    )
    row = cur.fetchone()
    
    if not row:
        db.close()
        db.close()
        # Retry! The DB might not be updated yet (New Product Race Condition)
        raise Exception(f"Product not found for blob {blob.name}. Retrying...")
    
    product_id = row[0]

    # 3. Check if tags already exist (Save Money!)
    cur.execute("SELECT COUNT(*) FROM product_tags WHERE product_id = ?", (product_id,))
    count = cur.fetchone()[0]

    if count > 0:
        db.close()
        return

    # 4. Only Call AI if NO tags exist
    vision = ImageAnalysisClient(
        os.environ["VISION_ENDPOINT"],
        AzureKeyCredential(os.environ["VISION_KEY"])
    )

    tags = vision.analyze(blob.read(), ["Tags"]).tags

    for t in tags:
        # Handle both object (t.name) and string (t) cases
        tag_name = t.name if hasattr(t, 'name') else str(t)
        cur.execute(
            "INSERT INTO product_tags (product_id, tag_name) VALUES (?, ?)",
            (product_id, tag_name)
        )

    db.commit()
    db.close()