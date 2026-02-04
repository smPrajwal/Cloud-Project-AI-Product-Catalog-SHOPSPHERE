import os

def seed_azure(conn):
    try:
        cursor = conn.cursor()
        
        # Base Image URL (Simple Check)
        acc = os.environ.get('STORAGE_ACCOUNT_NAME')
        base = f"https://{acc}.blob.core.windows.net/product-images/" if acc else "/static/product_images/"

        # Data Dictionary
        data = {
          "products": [
            {
              "id": 1,
              "name": "Aurum Sonic NC Headphones",
              "description": "",
              "price": 14999.0,
              "thumbnail_url": "/static/uploads/product_aurum-sonic-nc-headphones.jpg",
              "original_price": 20999
            },
            {
              "id": 2,
              "name": "ErgoMesh Pro Chair",
              "description": "",
              "price": 24999.0,
              "thumbnail_url": "/static/uploads/product_ergomesh-pro-chair.jpg?v=1767464900",
              "original_price": 39999
            },
            {
              "id": 3,
              "name": "Chronos Elite Smartwatch",
              "description": "Stay connected and fit with the Chronos Elite. Titanium casing, sapphire crystal glass, and advanced biometric sensors.",
              "price": 19999.0,
              "thumbnail_url": "/static/uploads/product_chronos-elite-smartwatch.jpg?v=1766687195",
              "original_price": 33999
            },
            {
              "id": 4,
              "name": "NeoVision 4K Monitor",
              "description": "Crystal clear 32-inch 4K UHD display with 144Hz refresh rate, perfect for creators and gamers alike.",
              "price": 45999.0,
              "thumbnail_url": "/static/uploads/product_neovision-4k-monitor.jpg",
              "original_price": 63999
            },
            {
              "id": 5,
              "name": "Zenith Mechanical Keyboard",
              "description": "Hot-swappable keys, RGB backlighting, and aircraft-grade aluminum frame.",
              "price": 8499.0,
              "thumbnail_url": "/static/uploads/product_zenith-mechanical-keyboard.jpg",
              "original_price": 14999
            },
            {
              "id": 6,
              "name": "SkyDrone X1",
              "description": "Capture stunning aerial footage with 4K camera and 30-minute flight time.",
              "price": 55999.0,
              "thumbnail_url": "/static/uploads/product_skydrone-x1.jpg",
              "original_price": 75999
            },
            {
              "id": 7,
              "name": "Nomad Leather Backpack",
              "description": "Handcrafted premium leather backpack with dedicated laptop compartment.",
              "price": 12999.0,
              "thumbnail_url": "/static/uploads/product_nomad-leather-backpack.jpg",
              "original_price": 21999
            },
            {
              "id": 8,
              "name": "PureFlow Water Bottle",
              "description": "Insulated stainless steel bottle keeps drinks cold for 24 hours.",
              "price": 1499.0,
              "thumbnail_url": "/static/uploads/product_pureflow-water-bottle.jpg",
              "original_price": 1999
            },
            {
              "id": 9,
              "name": "RetroInsta Camera",
              "description": "",
              "price": 7999.0,
              "thumbnail_url": "/static/uploads/product_retroinsta-camera.jpg",
              "original_price": 10999
            },
            {
              "id": 10,
              "name": "SolarPower Bank 20000",
              "description": "Rugged solar-charged power bank for your off-grid adventures.",
              "price": 3499.0,
              "thumbnail_url": "/static/uploads/product_solarpower-bank-20000.jpg",
              "original_price": 4999
            },
            {
              "id": 11,
              "name": "NutriBlend Pro Blender",
              "description": "High-performance countertop blender for smoothies, soups, and more.",
              "price": 4499.0,
              "thumbnail_url": "/static/uploads/product_nutriblend-pro-blender.jpg",
              "original_price": 6999
            },
            {
              "id": 12,
              "name": "BaristaExpress Coffee Maker",
              "description": "Brew cafe-quality espresso at home with this premium stainless steel machine.",
              "price": 12999.0,
              "thumbnail_url": "/static/uploads/product_baristaexpress-coffee-maker.jpg",
              "original_price": 21999
            },
            {
              "id": 13,
              "name": "ChefMaster Cookware Set",
              "description": "Complete non-stick cookware set with durable glass lids.",
              "price": 3499.0,
              "thumbnail_url": "/static/uploads/product_chefmaster-cookware-set.jpg",
              "original_price": 5499
            },
            {
              "id": 14,
              "name": "Classic Aviator Sunglasses",
              "description": "Timeless aviator design with gold frames and UV protection.",
              "price": 1499.0,
              "thumbnail_url": "/static/uploads/product_classic-aviator-sunglasses.jpg",
              "original_price": 1999
            },
            {
              "id": 15,
              "name": "Urban Denim Jacket",
              "description": "Vintage wash denim jacket, perfect for layering in any season.",
              "price": 2999.0,
              "thumbnail_url": "/static/uploads/product_urban-denim-jacket.jpg",
              "original_price": 5499
            },
            {
              "id": 16,
              "name": "ZenFlex Yoga Mat",
              "description": "Premium non-slip yoga mat with carrying strap for your daily practice.",
              "price": 999.0,
              "thumbnail_url": "/static/uploads/product_zenflex-yoga-mat.jpg",
              "original_price": 1499
            },
            {
              "id": 17,
              "name": "CloudRest Travel Pillow",
              "description": "Memory foam U-shaped pillow for ultimate comfort during travel.",
              "price": 1499.0,
              "thumbnail_url": "/static/uploads/product_cloudrest-travel-pillow.jpg",
              "original_price": 2499
            },
            {
              "id": 18,
              "name": "Executive Leather Notebook",
              "description": "Premium black leather notebook for your professional notes and ideas.",
              "price": 999.0,
              "thumbnail_url": "/static/uploads/product_executive-leather-notebook.jpg",
              "original_price": 1499
            },
            {
              "id": 19,
              "name": "Vintage Leather Belt",
              "description": "Durable genuine leather belt with a classic brass buckle.",
              "price": 799.0,
              "thumbnail_url": "/static/uploads/product_vintage-leather-belt.jpg",
              "original_price": 999
            },
            {
              "id": 20,
              "name": "Floral Silk Scarf",
              "description": "Elegant silk scarf with vibrant floral patterns.",
              "price": 1499.0,
              "thumbnail_url": "/static/uploads/product_floral-silk-scarf.jpg",
              "original_price": 1999
            },
            {
              "id": 21,
              "name": "Canvas High-Top Sneakers",
              "description": "Classic white high-top sneakers for everyday comfort and style.",
              "price": 2499.0,
              "thumbnail_url": "/static/uploads/product_canvas-high-top-sneakers.jpg",
              "original_price": 3999
            },
            {
              "id": 22,
              "name": "Bamboo Cutlery Set",
              "description": "Eco-friendly reusable bamboo fork, spoon, and knife set with pouch.",
              "price": 499.0,
              "thumbnail_url": "/static/uploads/product_bamboo-cutlery-set.jpg",
              "original_price": 799
            },
            {
              "id": 23,
              "name": "Aromatherapy Diffuser",
              "description": "Ultrasonic essential oil diffuser with soothing LED lights.",
              "price": 1999.0,
              "thumbnail_url": "/static/uploads/product_aromatherapy-diffuser.jpg",
              "original_price": 2499
            },
            {
              "id": 25,
              "name": "Ergonomic Vertical Mouse",
              "description": "Reduce wrist strain with this wireless vertical ergonomic mouse.",
              "price": 1499.0,
              "thumbnail_url": "/static/uploads/product_ergonomic-vertical-mouse.jpg",
              "original_price": 1999
            },
            {
              "id": 26,
              "name": "Aluminum Laptop Stand",
              "description": "Sturdy and sleek laptop stand for better ergonomics and cooling.",
              "price": 2999.0,
              "thumbnail_url": "/static/uploads/product_aluminum-laptop-stand.jpg",
              "original_price": 5499
            },
            {
              "id": 28,
              "name": "Digital Air Fryer",
              "description": "Healthier frying with little to no oil. 5L capacity with touch display.",
              "price": 5499.0,
              "thumbnail_url": "/static/uploads/product_digital-air-fryer.jpg",
              "original_price": 8999
            },
            {
              "id": 30,
              "name": "Pro Stand Mixer",
              "description": "Powerful 1000W mixer for baking needs. Includes dough hook and whisk.",
              "price": 18999.0,
              "thumbnail_url": "/static/uploads/product_pro-stand-mixer.jpg",
              "original_price": 24999
            },
            {
              "id": 31,
              "name": "2-Slice Toaster",
              "description": "Compact toaster with browning control and defrost function.",
              "price": 1999.0,
              "thumbnail_url": "/static/uploads/product_2-slice-toaster.jpg",
              "original_price": 2499
            },
            {
              "id": 33,
              "name": "Cold Press Juicer",
              "description": "Slow juicer to retain maximum nutrients from fruits and vegetables.",
              "price": 12999.0,
              "thumbnail_url": "/static/uploads/product_cold-press-juicer.jpg",
              "original_price": 16999
            },
            {
              "id": 34,
              "name": "Electric Kettle",
              "description": "Boil water in minutes. Stainless steel design.",
              "price": 1499.0,
              "thumbnail_url": "/static/uploads/product_electric-kettle.jpg",
              "original_price": 1999
            },
            {
              "id": 35,
              "name": "Microwave Oven",
              "description": "Quick heating and defrosting. Compact design.",
              "price": 5999.0,
              "thumbnail_url": "/static/uploads/product_microwave-oven.jpg",
              "original_price": 7999
            }
          ],
          "reviews": [
            {
              "id": 1,
              "product_id": 1,
              "reviewer": "AudioPhile99",
              "review_text": "The soundstage is incredible. Best ANC I've tried.",
              "sentiment_score": 0.9,
              "sentiment_label": "Positive"
            },
            {
              "id": 2,
              "product_id": 1,
              "reviewer": "Traveler",
              "review_text": "Saved me on my long flight. Comfortable for hours.",
              "sentiment_score": 0.85,
              "sentiment_label": "Positive"
            },
            {
              "id": 3,
              "product_id": 2,
              "reviewer": "DevLead",
              "review_text": "My back pain is gone since switching to this.",
              "sentiment_score": 0.95,
              "sentiment_label": "Positive"
            },
            {
              "id": 7,
              "product_id": 26,
              "reviewer": "prajwal",
              "review_text": "good",
              "sentiment_score": 0.5,
              "sentiment_label": "Neutral"
            },
            {
              "id": 11,
              "product_id": 7,
              "reviewer": "prajwal",
              "review_text": "good.",
              "sentiment_score": 0.5,
              "sentiment_label": "Neutral"
            },
            {
              "id": 12,
              "product_id": 10,
              "reviewer": "prajwal",
              "review_text": "good",
              "sentiment_score": 0.5,
              "sentiment_label": "Neutral"
            },
            {
              "id": 13,
              "product_id": 11,
              "reviewer": "prajwal",
              "review_text": "good.",
              "sentiment_score": 0.5,
              "sentiment_label": "Neutral"
            },
            {
              "id": 18,
              "product_id": 1,
              "reviewer": "Suresh_L",
              "review_text": "Super impressed with the build quality. Five stars!",
              "sentiment_score": 0.81,
              "sentiment_label": "Positive"
            },
            {
              "id": 19,
              "product_id": 1,
              "reviewer": "Karthik_N",
              "review_text": "Excellent value for money. Very happy with this purchase.",
              "sentiment_score": 0.81,
              "sentiment_label": "Positive"
            },
            {
              "id": 20,
              "product_id": 1,
              "reviewer": "Pooja_A",
              "review_text": "Excellent value for money. Very happy with this purchase.",
              "sentiment_score": 0.9,
              "sentiment_label": "Positive"
            },
            {
              "id": 21,
              "product_id": 1,
              "reviewer": "Amit_K",
              "review_text": "Best purchase I've made this year. Worth every rupee.",
              "sentiment_score": 0.81,
              "sentiment_label": "Positive"
            },
            {
              "id": 22,
              "product_id": 2,
              "reviewer": "Aditya_C",
              "review_text": "Absolutely love this product! Exceeded my expectations.",
              "sentiment_score": 0.88,
              "sentiment_label": "Positive"
            },
            {
              "id": 23,
              "product_id": 2,
              "reviewer": "Pooja_A",
              "review_text": "Cheap quality product. Don't buy.",
              "sentiment_score": 0.27,
              "sentiment_label": "Negative"
            },
            {
              "id": 24,
              "product_id": 2,
              "reviewer": "Vikram_R",
              "review_text": "Not satisfied at all. Poor customer experience.",
              "sentiment_score": 0.35,
              "sentiment_label": "Negative"
            },
            {
              "id": 25,
              "product_id": 2,
              "reviewer": "Swathi_P",
              "review_text": "It's alright. Serves its purpose.",
              "sentiment_score": 0.56,
              "sentiment_label": "Neutral"
            },
            {
              "id": 26,
              "product_id": 3,
              "reviewer": "Pooja_A",
              "review_text": "Standard quality. No complaints but nothing special.",
              "sentiment_score": 0.54,
              "sentiment_label": "Neutral"
            },
            {
              "id": 27,
              "product_id": 3,
              "reviewer": "Lakshmi_R",
              "review_text": "Quality is subpar. Not as advertised.",
              "sentiment_score": 0.27,
              "sentiment_label": "Negative"
            },
            {
              "id": 28,
              "product_id": 4,
              "reviewer": "Swathi_P",
              "review_text": "Absolutely love this product! Exceeded my expectations.",
              "sentiment_score": 0.92,
              "sentiment_label": "Positive"
            },
            {
              "id": 29,
              "product_id": 4,
              "reviewer": "Rahul_S",
              "review_text": "Poor build quality. Regret buying this.",
              "sentiment_score": 0.26,
              "sentiment_label": "Negative"
            },
            {
              "id": 30,
              "product_id": 4,
              "reviewer": "Meera_G",
              "review_text": "Good product but expected a bit more.",
              "sentiment_score": 0.49,
              "sentiment_label": "Neutral"
            },
            {
              "id": 31,
              "product_id": 4,
              "reviewer": "Arjun_B",
              "review_text": "Doesn't match the description at all.",
              "sentiment_score": 0.28,
              "sentiment_label": "Negative"
            },
            {
              "id": 32,
              "product_id": 5,
              "reviewer": "Kavitha_S",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.76,
              "sentiment_label": "Positive"
            },
            {
              "id": 33,
              "product_id": 5,
              "reviewer": "Lakshmi_R",
              "review_text": "Good product but expected a bit more.",
              "sentiment_score": 0.48,
              "sentiment_label": "Neutral"
            },
            {
              "id": 34,
              "product_id": 5,
              "reviewer": "Sneha_P",
              "review_text": "Absolutely love this product! Exceeded my expectations.",
              "sentiment_score": 0.93,
              "sentiment_label": "Positive"
            },
            {
              "id": 35,
              "product_id": 6,
              "reviewer": "Divya_K",
              "review_text": "It's alright. Serves its purpose.",
              "sentiment_score": 0.44,
              "sentiment_label": "Neutral"
            },
            {
              "id": 36,
              "product_id": 6,
              "reviewer": "Nikhil_J",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.9,
              "sentiment_label": "Positive"
            },
            {
              "id": 37,
              "product_id": 7,
              "reviewer": "Nikhil_J",
              "review_text": "Not worth the price. Expected better quality.",
              "sentiment_score": 0.2,
              "sentiment_label": "Negative"
            },
            {
              "id": 38,
              "product_id": 7,
              "reviewer": "Karthik_N",
              "review_text": "Outstanding quality. Definitely recommend to everyone.",
              "sentiment_score": 0.87,
              "sentiment_label": "Positive"
            },
            {
              "id": 39,
              "product_id": 7,
              "reviewer": "Swathi_P",
              "review_text": "Excellent value for money. Very happy with this purchase.",
              "sentiment_score": 0.84,
              "sentiment_label": "Positive"
            },
            {
              "id": 40,
              "product_id": 8,
              "reviewer": "Suresh_L",
              "review_text": "Decent product. Does what it's supposed to do.",
              "sentiment_score": 0.47,
              "sentiment_label": "Neutral"
            },
            {
              "id": 41,
              "product_id": 8,
              "reviewer": "Divya_K",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.89,
              "sentiment_label": "Positive"
            },
            {
              "id": 42,
              "product_id": 8,
              "reviewer": "Nikhil_J",
              "review_text": "Super impressed with the build quality. Five stars!",
              "sentiment_score": 0.78,
              "sentiment_label": "Positive"
            },
            {
              "id": 43,
              "product_id": 9,
              "reviewer": "Rohan_D",
              "review_text": "Super impressed with the build quality. Five stars!",
              "sentiment_score": 0.93,
              "sentiment_label": "Positive"
            },
            {
              "id": 44,
              "product_id": 9,
              "reviewer": "Suresh_L",
              "review_text": "Absolutely love this product! Exceeded my expectations.",
              "sentiment_score": 0.8,
              "sentiment_label": "Positive"
            },
            {
              "id": 45,
              "product_id": 9,
              "reviewer": "Arjun_B",
              "review_text": "Not worth the price. Expected better quality.",
              "sentiment_score": 0.27,
              "sentiment_label": "Negative"
            },
            {
              "id": 46,
              "product_id": 9,
              "reviewer": "Kavitha_S",
              "review_text": "Excellent value for money. Very happy with this purchase.",
              "sentiment_score": 0.94,
              "sentiment_label": "Positive"
            },
            {
              "id": 47,
              "product_id": 10,
              "reviewer": "Aditya_C",
              "review_text": "Perfect for my needs. Very satisfied with the quality.",
              "sentiment_score": 0.93,
              "sentiment_label": "Positive"
            },
            {
              "id": 48,
              "product_id": 10,
              "reviewer": "Anjali_T",
              "review_text": "Not worth the price. Expected better quality.",
              "sentiment_score": 0.31,
              "sentiment_label": "Negative"
            },
            {
              "id": 49,
              "product_id": 11,
              "reviewer": "Divya_K",
              "review_text": "Not worth the price. Expected better quality.",
              "sentiment_score": 0.3,
              "sentiment_label": "Negative"
            },
            {
              "id": 50,
              "product_id": 11,
              "reviewer": "Sanjay_M",
              "review_text": "Super impressed with the build quality. Five stars!",
              "sentiment_score": 0.9,
              "sentiment_label": "Positive"
            },
            {
              "id": 51,
              "product_id": 11,
              "reviewer": "Deepa_V",
              "review_text": "Absolutely love this product! Exceeded my expectations.",
              "sentiment_score": 0.92,
              "sentiment_label": "Positive"
            },
            {
              "id": 52,
              "product_id": 12,
              "reviewer": "Kavitha_S",
              "review_text": "Average quality. Meets basic requirements.",
              "sentiment_score": 0.42,
              "sentiment_label": "Neutral"
            },
            {
              "id": 53,
              "product_id": 12,
              "reviewer": "Sanjay_M",
              "review_text": "Perfect for my needs. Very satisfied with the quality.",
              "sentiment_score": 0.82,
              "sentiment_label": "Positive"
            },
            {
              "id": 54,
              "product_id": 13,
              "reviewer": "Suresh_L",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.93,
              "sentiment_label": "Positive"
            },
            {
              "id": 55,
              "product_id": 13,
              "reviewer": "Lakshmi_R",
              "review_text": "Cheap quality product. Don't buy.",
              "sentiment_score": 0.28,
              "sentiment_label": "Negative"
            },
            {
              "id": 56,
              "product_id": 13,
              "reviewer": "Arjun_B",
              "review_text": "Average quality. Meets basic requirements.",
              "sentiment_score": 0.48,
              "sentiment_label": "Neutral"
            },
            {
              "id": 57,
              "product_id": 13,
              "reviewer": "Nikhil_J",
              "review_text": "Product is acceptable. Packaging could be better.",
              "sentiment_score": 0.42,
              "sentiment_label": "Neutral"
            },
            {
              "id": 58,
              "product_id": 14,
              "reviewer": "Swathi_P",
              "review_text": "Best purchase I've made this year. Worth every rupee.",
              "sentiment_score": 0.86,
              "sentiment_label": "Positive"
            },
            {
              "id": 59,
              "product_id": 14,
              "reviewer": "Lakshmi_R",
              "review_text": "Best purchase I've made this year. Worth every rupee.",
              "sentiment_score": 0.78,
              "sentiment_label": "Positive"
            },
            {
              "id": 60,
              "product_id": 14,
              "reviewer": "Meera_G",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.76,
              "sentiment_label": "Positive"
            },
            {
              "id": 61,
              "product_id": 15,
              "reviewer": "Swathi_P",
              "review_text": "Moderate quality. Would consider other options next time.",
              "sentiment_score": 0.48,
              "sentiment_label": "Neutral"
            },
            {
              "id": 62,
              "product_id": 15,
              "reviewer": "Pooja_A",
              "review_text": "Moderate quality. Would consider other options next time.",
              "sentiment_score": 0.43,
              "sentiment_label": "Neutral"
            },
            {
              "id": 63,
              "product_id": 15,
              "reviewer": "Divya_K",
              "review_text": "Absolutely love this product! Exceeded my expectations.",
              "sentiment_score": 0.77,
              "sentiment_label": "Positive"
            },
            {
              "id": 64,
              "product_id": 16,
              "reviewer": "Lakshmi_R",
              "review_text": "Excellent value for money. Very happy with this purchase.",
              "sentiment_score": 0.86,
              "sentiment_label": "Positive"
            },
            {
              "id": 65,
              "product_id": 16,
              "reviewer": "Aditya_C",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.8,
              "sentiment_label": "Positive"
            },
            {
              "id": 66,
              "product_id": 16,
              "reviewer": "Sanjay_M",
              "review_text": "Had to return it. Complete waste of time.",
              "sentiment_score": 0.24,
              "sentiment_label": "Negative"
            },
            {
              "id": 67,
              "product_id": 16,
              "reviewer": "Suresh_L",
              "review_text": "Fantastic product! My whole family loves it.",
              "sentiment_score": 0.81,
              "sentiment_label": "Positive"
            },
            {
              "id": 68,
              "product_id": 17,
              "reviewer": "Meera_G",
              "review_text": "Fantastic product! My whole family loves it.",
              "sentiment_score": 0.89,
              "sentiment_label": "Positive"
            },
            {
              "id": 69,
              "product_id": 17,
              "reviewer": "Kavitha_S",
              "review_text": "Very disappointed. Save your money.",
              "sentiment_score": 0.33,
              "sentiment_label": "Negative"
            },
            {
              "id": 70,
              "product_id": 18,
              "reviewer": "Karthik_N",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.88,
              "sentiment_label": "Positive"
            },
            {
              "id": 71,
              "product_id": 18,
              "reviewer": "Rohan_D",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.77,
              "sentiment_label": "Positive"
            },
            {
              "id": 72,
              "product_id": 18,
              "reviewer": "Kavitha_S",
              "review_text": "Works perfectly and looks great. Couldn't be happier.",
              "sentiment_score": 0.91,
              "sentiment_label": "Positive"
            },
            {
              "id": 73,
              "product_id": 19,
              "reviewer": "Nikhil_J",
              "review_text": "Best purchase I've made this year. Worth every rupee.",
              "sentiment_score": 0.81,
              "sentiment_label": "Positive"
            },
            {
              "id": 74,
              "product_id": 19,
              "reviewer": "Karthik_N",
              "review_text": "Best purchase I've made this year. Worth every rupee.",
              "sentiment_score": 0.89,
              "sentiment_label": "Positive"
            },
            {
              "id": 75,
              "product_id": 19,
              "reviewer": "Swathi_P",
              "review_text": "Outstanding quality. Definitely recommend to everyone.",
              "sentiment_score": 0.78,
              "sentiment_label": "Positive"
            },
            {
              "id": 76,
              "product_id": 20,
              "reviewer": "Priya_M",
              "review_text": "Product is acceptable. Packaging could be better.",
              "sentiment_score": 0.41,
              "sentiment_label": "Neutral"
            },
            {
              "id": 77,
              "product_id": 20,
              "reviewer": "Aditya_C",
              "review_text": "Good product but expected a bit more.",
              "sentiment_score": 0.48,
              "sentiment_label": "Neutral"
            },
            {
              "id": 78,
              "product_id": 21,
              "reviewer": "Lakshmi_R",
              "review_text": "Quality is subpar. Not as advertised.",
              "sentiment_score": 0.34,
              "sentiment_label": "Negative"
            },
            {
              "id": 79,
              "product_id": 21,
              "reviewer": "Rohan_D",
              "review_text": "Decent product. Does what it's supposed to do.",
              "sentiment_score": 0.52,
              "sentiment_label": "Neutral"
            },
            {
              "id": 80,
              "product_id": 21,
              "reviewer": "Divya_K",
              "review_text": "Had to return it. Complete waste of time.",
              "sentiment_score": 0.17,
              "sentiment_label": "Negative"
            },
            {
              "id": 81,
              "product_id": 22,
              "reviewer": "Amit_K",
              "review_text": "Had to return it. Complete waste of time.",
              "sentiment_score": 0.28,
              "sentiment_label": "Negative"
            },
            {
              "id": 82,
              "product_id": 22,
              "reviewer": "Rahul_S",
              "review_text": "Highly recommended! You won't regret it.",
              "sentiment_score": 0.84,
              "sentiment_label": "Positive"
            },
            {
              "id": 83,
              "product_id": 22,
              "reviewer": "Suresh_L",
              "review_text": "Perfect for my needs. Very satisfied with the quality.",
              "sentiment_score": 0.85,
              "sentiment_label": "Positive"
            },
            {
              "id": 84,
              "product_id": 23,
              "reviewer": "Aditya_C",
              "review_text": "Works perfectly and looks great. Couldn't be happier.",
              "sentiment_score": 0.92,
              "sentiment_label": "Positive"
            },
            {
              "id": 85,
              "product_id": 23,
              "reviewer": "Vikram_R",
              "review_text": "Quality is subpar. Not as advertised.",
              "sentiment_score": 0.28,
              "sentiment_label": "Negative"
            },
            {
              "id": 86,
              "product_id": 23,
              "reviewer": "Meera_G",
              "review_text": "Fantastic product! My whole family loves it.",
              "sentiment_score": 0.82,
              "sentiment_label": "Positive"
            },
            {
              "id": 90,
              "product_id": 25,
              "reviewer": "Anjali_T",
              "review_text": "Moderate quality. Would consider other options next time.",
              "sentiment_score": 0.42,
              "sentiment_label": "Neutral"
            },
            {
              "id": 91,
              "product_id": 25,
              "reviewer": "Nikhil_J",
              "review_text": "Fantastic product! My whole family loves it.",
              "sentiment_score": 0.86,
              "sentiment_label": "Positive"
            },
            {
              "id": 92,
              "product_id": 25,
              "reviewer": "Pooja_A",
              "review_text": "Not satisfied at all. Poor customer experience.",
              "sentiment_score": 0.35,
              "sentiment_label": "Negative"
            },
            {
              "id": 93,
              "product_id": 26,
              "reviewer": "Swathi_P",
              "review_text": "Does the job.",
              "sentiment_score": 0.61,
              "sentiment_label": "Positive"
            },
            {
              "id": 94,
              "product_id": 26,
              "reviewer": "Arjun_B",
              "review_text": "Very disappointed. Save your money.",
              "sentiment_score": 0.21,
              "sentiment_label": "Negative"
            },
            {
              "id": 95,
              "product_id": 26,
              "reviewer": "Pooja_A",
              "review_text": "Average quality. Meets basic requirements.",
              "sentiment_score": 0.52,
              "sentiment_label": "Neutral"
            },
            {
              "id": 99,
              "product_id": 28,
              "reviewer": "Kavitha_S",
              "review_text": "Excellent value for money. Very happy with this purchase.",
              "sentiment_score": 0.88,
              "sentiment_label": "Positive"
            },
            {
              "id": 100,
              "product_id": 28,
              "reviewer": "Karthik_N",
              "review_text": "Perfect for my needs. Very satisfied with the quality.",
              "sentiment_score": 0.85,
              "sentiment_label": "Positive"
            },
            {
              "id": 101,
              "product_id": 28,
              "reviewer": "Rahul_S",
              "review_text": "Does the job.",
              "sentiment_score": 0.62,
              "sentiment_label": "Positive"
            },
            {
              "id": 105,
              "product_id": 30,
              "reviewer": "Priya_M",
              "review_text": "Works perfectly and looks great. Couldn't be happier.",
              "sentiment_score": 0.86,
              "sentiment_label": "Positive"
            },
            {
              "id": 106,
              "product_id": 30,
              "reviewer": "Aditya_C",
              "review_text": "Poor build quality. Regret buying this.",
              "sentiment_score": 0.21,
              "sentiment_label": "Negative"
            },
            {
              "id": 107,
              "product_id": 30,
              "reviewer": "Sneha_P",
              "review_text": "Does the job.",
              "sentiment_score": 0.58,
              "sentiment_label": "Neutral"
            },
            {
              "id": 108,
              "product_id": 31,
              "reviewer": "Suresh_L",
              "review_text": "Fantastic product! My whole family loves it.",
              "sentiment_score": 0.8,
              "sentiment_label": "Positive"
            },
            {
              "id": 109,
              "product_id": 31,
              "reviewer": "Amit_K",
              "review_text": "Decent product. Does what it's supposed to do.",
              "sentiment_score": 0.44,
              "sentiment_label": "Neutral"
            },
            {
              "id": 110,
              "product_id": 31,
              "reviewer": "Rahul_S",
              "review_text": "Not worth the price. Expected better quality.",
              "sentiment_score": 0.28,
              "sentiment_label": "Negative"
            },
            {
              "id": 114,
              "product_id": 33,
              "reviewer": "Anjali_T",
              "review_text": "Surprisingly good quality for the price.",
              "sentiment_score": 0.73,
              "sentiment_label": "Positive"
            },
            {
              "id": 115,
              "product_id": 33,
              "reviewer": "Amit_K",
              "review_text": "Fantastic product! My whole family loves it.",
              "sentiment_score": 0.87,
              "sentiment_label": "Positive"
            },
            {
              "id": 116,
              "product_id": 33,
              "reviewer": "Lakshmi_R",
              "review_text": "Had to return it. Complete waste of time.",
              "sentiment_score": 0.24,
              "sentiment_label": "Negative"
            },
            {
              "id": 117,
              "product_id": 34,
              "reviewer": "Suresh_L",
              "review_text": "It's alright. Serves its purpose.",
              "sentiment_score": 0.55,
              "sentiment_label": "Neutral"
            },
            {
              "id": 118,
              "product_id": 34,
              "reviewer": "Lakshmi_R",
              "review_text": "Amazing product! Will definitely buy again.",
              "sentiment_score": 0.81,
              "sentiment_label": "Positive"
            },
            {
              "id": 119,
              "product_id": 34,
              "reviewer": "Pooja_A",
              "review_text": "Moderate quality. Would consider other options next time.",
              "sentiment_score": 0.43,
              "sentiment_label": "Neutral"
            },
            {
              "id": 120,
              "product_id": 35,
              "reviewer": "Rahul_S",
              "review_text": "Super impressed with the build quality. Five stars!",
              "sentiment_score": 0.83,
              "sentiment_label": "Positive"
            },
            {
              "id": 121,
              "product_id": 35,
              "reviewer": "Amit_K",
              "review_text": "Cheap quality product. Don't buy.",
              "sentiment_score": 0.26,
              "sentiment_label": "Negative"
            },
            {
              "id": 122,
              "product_id": 35,
              "reviewer": "Kavitha_S",
              "review_text": "Good product but expected a bit more.",
              "sentiment_score": 0.42,
              "sentiment_label": "Neutral"
            }
          ],
          "product_tags": [
            {
              "id": 1,
              "product_id": 1,
              "tag_name": "audio"
            },
            {
              "id": 2,
              "product_id": 1,
              "tag_name": "tech"
            },
            {
              "id": 3,
              "product_id": 2,
              "tag_name": "furniture"
            },
            {
              "id": 4,
              "product_id": 2,
              "tag_name": "office"
            },
            {
              "id": 5,
              "product_id": 3,
              "tag_name": "tech"
            },
            {
              "id": 6,
              "product_id": 3,
              "tag_name": "lifestyle"
            },
            {
              "id": 7,
              "product_id": 4,
              "tag_name": "tech"
            },
            {
              "id": 8,
              "product_id": 4,
              "tag_name": "monitor"
            },
            {
              "id": 9,
              "product_id": 5,
              "tag_name": "tech"
            },
            {
              "id": 10,
              "product_id": 5,
              "tag_name": "office"
            },
            {
              "id": 11,
              "product_id": 6,
              "tag_name": "tech"
            },
            {
              "id": 12,
              "product_id": 6,
              "tag_name": "lifestyle"
            },
            {
              "id": 13,
              "product_id": 7,
              "tag_name": "fashion"
            },
            {
              "id": 14,
              "product_id": 7,
              "tag_name": "travel"
            },
            {
              "id": 15,
              "product_id": 8,
              "tag_name": "lifestyle"
            },
            {
              "id": 16,
              "product_id": 8,
              "tag_name": "eco"
            },
            {
              "id": 17,
              "product_id": 9,
              "tag_name": "tech"
            },
            {
              "id": 18,
              "product_id": 9,
              "tag_name": "lifestyle"
            },
            {
              "id": 19,
              "product_id": 10,
              "tag_name": "tech"
            },
            {
              "id": 20,
              "product_id": 10,
              "tag_name": "travel"
            },
            {
              "id": 21,
              "product_id": 11,
              "tag_name": "kitchen"
            },
            {
              "id": 22,
              "product_id": 11,
              "tag_name": "home"
            },
            {
              "id": 23,
              "product_id": 12,
              "tag_name": "kitchen"
            },
            {
              "id": 24,
              "product_id": 12,
              "tag_name": "lifestyle"
            },
            {
              "id": 25,
              "product_id": 13,
              "tag_name": "kitchen"
            },
            {
              "id": 26,
              "product_id": 13,
              "tag_name": "home"
            },
            {
              "id": 27,
              "product_id": 14,
              "tag_name": "fashion"
            },
            {
              "id": 28,
              "product_id": 14,
              "tag_name": "accessories"
            },
            {
              "id": 29,
              "product_id": 15,
              "tag_name": "fashion"
            },
            {
              "id": 30,
              "product_id": 15,
              "tag_name": "clothing"
            },
            {
              "id": 31,
              "product_id": 16,
              "tag_name": "lifestyle"
            },
            {
              "id": 32,
              "product_id": 16,
              "tag_name": "fitness"
            },
            {
              "id": 33,
              "product_id": 17,
              "tag_name": "travel"
            },
            {
              "id": 34,
              "product_id": 17,
              "tag_name": "lifestyle"
            },
            {
              "id": 35,
              "product_id": 18,
              "tag_name": "office"
            },
            {
              "id": 36,
              "product_id": 18,
              "tag_name": "lifestyle"
            },
            {
              "id": 37,
              "product_id": 19,
              "tag_name": "fashion"
            },
            {
              "id": 38,
              "product_id": 19,
              "tag_name": "accessories"
            },
            {
              "id": 39,
              "product_id": 20,
              "tag_name": "fashion"
            },
            {
              "id": 40,
              "product_id": 20,
              "tag_name": "accessories"
            },
            {
              "id": 41,
              "product_id": 21,
              "tag_name": "fashion"
            },
            {
              "id": 42,
              "product_id": 21,
              "tag_name": "shoes"
            },
            {
              "id": 43,
              "product_id": 22,
              "tag_name": "kitchen"
            },
            {
              "id": 44,
              "product_id": 22,
              "tag_name": "eco"
            },
            {
              "id": 45,
              "product_id": 23,
              "tag_name": "home"
            },
            {
              "id": 46,
              "product_id": 23,
              "tag_name": "lifestyle"
            },
            {
              "id": 49,
              "product_id": 25,
              "tag_name": "tech"
            },
            {
              "id": 50,
              "product_id": 25,
              "tag_name": "office"
            },
            {
              "id": 51,
              "product_id": 26,
              "tag_name": "tech"
            },
            {
              "id": 52,
              "product_id": 26,
              "tag_name": "office"
            },
            {
              "id": 55,
              "product_id": 28,
              "tag_name": "kitchen"
            },
            {
              "id": 56,
              "product_id": 28,
              "tag_name": "home"
            },
            {
              "id": 59,
              "product_id": 30,
              "tag_name": "kitchen"
            },
            {
              "id": 60,
              "product_id": 30,
              "tag_name": "baking"
            },
            {
              "id": 61,
              "product_id": 31,
              "tag_name": "kitchen"
            },
            {
              "id": 62,
              "product_id": 31,
              "tag_name": "home"
            },
            {
              "id": 65,
              "product_id": 33,
              "tag_name": "kitchen"
            },
            {
              "id": 66,
              "product_id": 33,
              "tag_name": "health"
            },
            {
              "id": 67,
              "product_id": 34,
              "tag_name": "kitchen"
            },
            {
              "id": 68,
              "product_id": 34,
              "tag_name": "home"
            },
            {
              "id": 69,
              "product_id": 35,
              "tag_name": "kitchen"
            },
            {
              "id": 70,
              "product_id": 35,
              "tag_name": "home"
            }
          ]
        }
        
        # --- Seed Products ---
        print("Checking Products...")
        if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
            print("Seeding Products...")
            cursor.execute("SET IDENTITY_INSERT products ON")
            for p in data['products']:
                img = base + p['thumbnail_url'].split('/')[-1]
                cursor.execute(
                    "INSERT INTO products (id, name, description, price, original_price, thumbnail_url) VALUES (?, ?, ?, ?, ?, ?)",
                    (p['id'], p['name'], p['description'], p['price'], p['original_price'], img)
                )
            cursor.execute("SET IDENTITY_INSERT products OFF")
            print("Products seeded.")
            
        # --- Seed Reviews ---
        print("Checking Reviews...")
        if cursor.execute("SELECT COUNT(*) FROM reviews").fetchone()[0] == 0:
            print("Seeding Reviews...")
            cursor.execute("SET IDENTITY_INSERT reviews ON")
            for r in data['reviews']:
                cursor.execute(
                    "INSERT INTO reviews (id, product_id, reviewer, review_text, sentiment_score, sentiment_label) VALUES (?, ?, ?, ?, ?, ?)",
                    (r['id'], r['product_id'], r['reviewer'], r['review_text'], r['sentiment_score'], r['sentiment_label'])
                )
            cursor.execute("SET IDENTITY_INSERT reviews OFF")
            print("Reviews seeded.")

        # --- Seed Tags ---
        print("Checking Tags...")
        if cursor.execute("SELECT COUNT(*) FROM product_tags").fetchone()[0] == 0:
            print("Seeding Tags...")
            cursor.execute("SET IDENTITY_INSERT product_tags ON")
            for t in data['product_tags']:
                cursor.execute(
                    "INSERT INTO product_tags (id, product_id, tag_name) VALUES (?, ?, ?)",
                    (t['id'], t['product_id'], t['tag_name'])
                )
            cursor.execute("SET IDENTITY_INSERT product_tags OFF")
            print("Tags seeded.")

        conn.commit()
    except Exception as e:
        print(f"Seeding Error: {e}")

