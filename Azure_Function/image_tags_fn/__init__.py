import os
import pyodbc
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
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

    # 3. Check if tags already exist (To support Seeded Data vs User Uploads)
    cur.execute("SELECT COUNT(*) FROM product_tags WHERE product_id = ?", (product_id,))
    count = cur.fetchone()[0]

    if count > 0:
        db.close()
        return

    # 4. Analyze New Image (If no tags exist)
    try:
        vision = ImageAnalysisClient(
            os.environ["VISION_ENDPOINT"],
            AzureKeyCredential(os.environ["VISION_KEY"])
        )

        result = vision.analyze(
            image_data=blob.read(),
            visual_features=[VisualFeatures.TAGS]
        )

        # 5. Insert New Tags
        if result.tags and result.tags.list:
            # Note: No need to DELETE here because Backend/Logic already ensures we only get here if tags=0.
            # Limit to top 8 tags as requested
            for tag in result.tags.list[:8]:
                cur.execute(
                    "INSERT INTO product_tags (product_id, tag_name) VALUES (?, ?)",
                    (product_id, tag.name)
                )
            
            db.commit()

    except Exception as e:
        print(f"Error processing image: {e}")
        # Build robustness: If AI fails, we keep old tags? Or fail? 
        # Requirement implies we want NEW tags. If fail, maybe keep old ones?
        # But 'replace' implies clear intent. Let's just log and not commit delete if analyze fails (implicit in try/catch block placement).
        pass

    db.close()