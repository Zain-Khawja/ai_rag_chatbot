import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
input_file = os.path.join(base_dir, "data", "knowledge_base.json")
output_dir = os.path.join(base_dir, "data", "json_batches")

def split_json_file():
    os.makedirs(output_dir, exist_ok=True)
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, list):
        for i in range(0, len(data), 50):
            batch = data[i:i + 50]
            batch_file = os.path.join(output_dir, f'batch_{i//50 + 1}.json')
            with open(batch_file, 'w', encoding='utf-8') as f:
                json.dump(batch, f, indent=2, ensure_ascii=False)
            print(f"Created {batch_file} with {len(batch)} items")

if __name__ == "__main__":
    split_json_file()
