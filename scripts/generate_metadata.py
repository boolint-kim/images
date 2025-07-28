import os, json
from PIL import Image

BASE_DIR = "."  # 현재 디렉토리에서 시작
METADATA_FILE = "metadata.json"
BASE_URL = "https://raw.githubusercontent.com/boolint-kim/images/main"

def generate_thumbnail(input_path, output_path, size=(200, 200)):
    img = Image.open(input_path)
    img.thumbnail(size)
    img.save(output_path, "JPEG")

def main():
    metadata = []

    for category in os.listdir(BASE_DIR):
        category_path = os.path.join(BASE_DIR, category)
        if not os.path.isdir(category_path):
            continue

        full_dir = os.path.join(category_path, "full")
        thumb_dir = os.path.join(category_path, "thumbs")
        if not os.path.exists(full_dir):
            continue

        os.makedirs(thumb_dir, exist_ok=True)

        for fname in os.listdir(full_dir):
            if not fname.lower().endswith((".jpg", ".jpeg", ".png")):
                continue

            id = os.path.splitext(fname)[0]
            thumb_name = f"{id}_thumb.jpg"
            thumb_path = os.path.join(thumb_dir, thumb_name)
            full_path = os.path.join(full_dir, fname)

            try:
                generate_thumbnail(full_path, thumb_path)
            except Exception as e:
                print(f"⚠️ Failed to generate thumbnail for {fname}: {e}")
                continue

            metadata.append({
                "id": id,
                "category": category,
                "thumbUrl": f"{BASE_URL}/{category}/thumbs/{thumb_name}",
                "fullUrl": f"{BASE_URL}/{category}/full/{fname}"
            })

    with open(METADATA_FILE, "w") as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main()
