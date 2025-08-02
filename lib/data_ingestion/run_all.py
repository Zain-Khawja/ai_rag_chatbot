# run_all.py
import subprocess
import os

def run_python(file_path):
    print(f"\n🚀 Running: {file_path}")
    # Run from project root directory to ensure proper module imports
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = subprocess.run(["python", file_path], capture_output=True, text=True, cwd=project_root)
    print(result.stdout)
    if result.stderr:
        print("❌ Error:", result.stderr)

# Define paths - all files are in the same directory as this script
base_dir = os.path.dirname(os.path.abspath(__file__))

steps = [
    os.path.join(base_dir, "fetch_products.py"),
    os.path.join(base_dir, "fetch_static_pages.py"),
    os.path.join(base_dir, "merge_knowledge.py"),
    os.path.join(base_dir, "split_json.py"),
    os.path.join(base_dir, "ingest.py")
]

if __name__ == "__main__":
    for step in steps:
        run_python(step)
