# merge_knowledge.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import json

data_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'data')
product_file = os.path.join(data_dir, "woocommerce_data.json")
static_file = os.path.join(data_dir, "static_pages.json")
output_file = os.path.join(data_dir, "knowledge_base.json")

def merge_files():
    with open(product_file, 'r', encoding='utf-8') as f1, open(static_file, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
        merged = data1 + data2
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(merged, out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    merge_files()
