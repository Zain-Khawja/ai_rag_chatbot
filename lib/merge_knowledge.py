# merge_knowledge.py
import json

def merge_files(product_file, static_file, output_file):
    with open(product_file, 'r', encoding='utf-8') as f1, open(static_file, 'r', encoding='utf-8') as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)
        merged = data1 + data2
    with open(output_file, 'w', encoding='utf-8') as out:
        json.dump(merged, out, indent=2, ensure_ascii=False)

merge_files("woocommerce_data.json", "static_pages.json", "knowledge_base.json")
