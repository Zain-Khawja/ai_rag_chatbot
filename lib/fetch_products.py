# fetch_products.py
import requests, json
from lib.config import WOOCOMMERCE_CK, WOOCOMMERCE_CS

BASE_URL = "https://aaasafedubai.com/wp-json/wc/v3/products"
CK = WOOCOMMERCE_CK
CS = WOOCOMMERCE_CS

def fetch_all():
    all_data, page = [], 1
    while True:
        res = requests.get(BASE_URL, params={
            'consumer_key': CK, 'consumer_secret': CS,
            'per_page': 100, 'page': page
        })
        
        print(f"Fetching page {page}...")
        
        
        products = res.json()
        if not products: break

        for p in products:
            variations_info = []

            # If it's a variable product, get variations
            if p.get("type") == "variable":
                var_res = requests.get(
                    f"{BASE_URL}/{p['id']}/variations",
                    params={'consumer_key': CK, 'consumer_secret': CS}
                )
                variations = var_res.json()
                for v in variations:
                    variations_info.append({
                        "sku": v.get("sku"),
                        "price": v.get("price"),
                        "attributes": v.get("attributes")
                    })

            product_entry = {
                "title": p.get("name"),
                "body": (
                    f"{p.get('description', '')}\n\n"
                    f"Price: ₹{p.get('price', 'N/A')}\n"
                    f"SKU: {p.get('sku', 'N/A')}\n"
                    f"Stock: {p.get('stock_status', 'N/A')}\n"
                    f"Type: {p.get('type')}\n"
                    f"Categories: {', '.join([c['name'] for c in p.get('categories', [])])}\n"
                    f"Attributes: {p.get('attributes', [])}\n"
                    f"Variations: {variations_info if variations_info else 'None'}"
                )
            }
            all_data.append(product_entry)
        page += 1

    with open("woocommerce_data.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    fetch_all()
