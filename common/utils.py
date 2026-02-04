import os
import requests

# 1. AI Analysis
def analyze_sentiment(text):
    endpoint = os.environ.get('AZURE_AI_ENDPOINT')
    key = os.environ.get('AZURE_AI_KEY')
    
    if not (endpoint and key): return {'score': 0.5, 'label': 'Neutral'}

    try:
        # Call Azure AI
        url = f"{endpoint}/text/analytics/v3.1/sentiment"
        resp = requests.post(url, headers={"Ocp-Apim-Subscription-Key": key}, json={"documents": [{"id": "1", "text": text}]})
        
        # Get Result
        tag = resp.json()['documents'][0]['sentiment']
        score = {'positive': 0.9, 'negative': 0.1}.get(tag, 0.5)
        
        return {'score': score, 'label': tag.capitalize()}
    except:
        return {'score': 0.5, 'label': 'Error'}

# 2. Image Upload
def upload_product_image(file, name):
    try:
        from azure.storage.blob import BlobServiceClient
        
        # Connect to Azure
        connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
        client = BlobServiceClient.from_connection_string(connect_str)
        
        # Create Filename & Upload
        filename = f"product_{name}.jpg"
        blob = client.get_blob_client("product-images", filename)
        
        file.seek(0) # Make sure we read from start
        blob.upload_blob(file.read(), overwrite=True)
        
        return blob.url, filename
    except Exception as e:
        print(f"Upload Error: {e}")
        return None, None

# 3. Currency Format (Indian Style: 1,00,000)
def format_indian_currency(value):
    s = str(int(value))
    if len(s) <= 3: return s
    
    # 12345 -> 12,345 | 1234567 -> 12,34,567
    last_3 = s[-3:]
    rest = s[:-3]
    
    # Add commas to the rest every 2 digits
    formatted = ""
    while len(rest) > 2:
        formatted = "," + rest[-2:] + formatted
        rest = rest[:-2]
        
    return rest + formatted + "," + last_3


