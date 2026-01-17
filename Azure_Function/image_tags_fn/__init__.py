import os
import pyodbc
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential

def main(blob):
    vision = ImageAnalysisClient(
        os.environ["VISION_ENDPOINT"],
        AzureKeyCredential(os.environ["VISION_KEY"])
    )

    tags = vision.analyze(blob.read(), ["Tags"]).tags

    db = pyodbc.connect(os.environ["AZURE_SQL_CONN"])
    cur = db.cursor()

    cur.execute(
        "SELECT id FROM products WHERE thumbnail_url LIKE ?",
        ("%" + blob.name,)
    )

    row = cur.fetchone()
    if not row:
        return
    
    product_id = row[0]

    cur.execute(
        "DELETE FROM product_tags WHERE product_id = ?",
        (product_id,)
    )

    for t in tags:
        cur.execute(
            "INSERT INTO product_tags (product_id, tag_name) VALUES (?, ?)",
            (product_id, t.name)
        )

    db.commit()
    db.close()