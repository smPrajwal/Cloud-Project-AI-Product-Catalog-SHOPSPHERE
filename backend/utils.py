import os
from database.db import get_db

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Azure Stubs
import requests

def analyze_sentiment(text):
    endpoint = os.environ.get('AZURE_AI_ENDPOINT')
    key = os.environ.get('AZURE_AI_KEY')
    
    # If no keys, just return a fake neutral result (keeps app working locally)
    if not endpoint or not key:
        return {'score': 0.5, 'label': 'Neutral (Local)'}

    try:
        # Simple API call
        url = f"{endpoint}/text/analytics/v3.1/sentiment"
        headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
        data = {"documents": [{"id": "1", "language": "en", "text": text}]}
        
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # Get the answer
        doc = result['documents'][0]
        sentiment = doc['sentiment']
        
        # Convert 'positive'/'negative' to a simple number (0 to 1)
        score = 0.5
        if sentiment == 'positive':
            score = 0.9
        elif sentiment == 'negative':
            score = 0.1
            
        return {'score': score, 'label': sentiment.capitalize()}
        
    except Exception as e:
        print("AI Error:", e)
        return {'score': 0.5, 'label': 'Error'}

def upload_product_image(file, slug):
    filename = f"product_{slug}.jpg"
    
    # 1. Save Locally (Safe Write)
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    try:
        with open(local_path, "wb") as f:
            f.write(file.read())
    except Exception as e:
        print(f"File Write Error: {e}")
        return None, None

    # 2. Azure Upload (Optional)
    blob_name = None
    if os.environ.get('USE_AZURE_BLOB') == 'true':
        try:
            from azure.storage.blob import BlobServiceClient
            conn_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
            if conn_str:
                client = BlobServiceClient.from_connection_string(conn_str)
                blob = client.get_blob_client(container="product-images", blob=filename)
                with open(local_path, "rb") as data:
                    blob.upload_blob(data, overwrite=True)
                print(f"LOG: Uploaded blob {filename}")
                return blob.url, filename
        except Exception as e:
            print(f"Azure Upload Failed: {e}")
            
    # Default: Return local path
    return f"/{local_path}".replace("\\", "/"), None



def format_indian_currency(value):
    try:
        value = int(float(value)) 
    except (ValueError, TypeError):
        return value
    
    s = str(value)
    if len(s) <= 3:
        return s
    
    last_three = s[-3:]
    rest = s[:-3]
    
    parts = []
    while rest:
        parts.append(rest[-2:])
        rest = rest[:-2]
    
    parts.reverse()
    return ",".join(parts) + "," + last_three

from functools import lru_cache

@lru_cache(maxsize=1)
def get_footer_settings():
    """Helper to get footer settings from database"""
    db = get_db()
    settings = db.execute('SELECT key, value FROM site_settings WHERE key LIKE "footer_%"').fetchall()
    return {row['key']: row['value'] for row in settings}
