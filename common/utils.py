import os


UPLOAD_FOLDER = 'frontend/static/product_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Azure Stubs
import requests

def analyze_sentiment(text):
    endpoint = os.environ.get('AZURE_AI_ENDPOINT')
    key = os.environ.get('AZURE_AI_KEY')
    
    # If no keys, return generic Neutral
    if not endpoint or not key:
        return {'score': 0.5, 'label': 'Neutral'}

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
    local_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # 1. Save Temp (For upload)
    with open(local_path, "wb") as f:
        f.write(file.read())
        
    # 2. Azure Blob Upload (Required)
    try:
        from azure.storage.blob import BlobServiceClient
        conn = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        if not conn:
             raise Exception("AZURE_STORAGE_CONNECTION_STRING not set")

        client = BlobServiceClient.from_connection_string(conn)
        client.get_blob_client("product-images", filename).upload_blob(open(local_path, "rb"), overwrite=True)
        
        # Cleanup temp file
        try: os.remove(local_path)
        except: pass

        return f"https://{client.account_name}.blob.core.windows.net/product-images/{filename}", filename
    except Exception as e:
        print("Cloud Upload Error:", e)
        raise e



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


