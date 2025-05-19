import imagehash
from PIL import Image
import json

def verify_image_phash(image_path, json_path, nft_id):
    # Load image and compute phash
    image = Image.open(image_path)
    computed_phash = str(imagehash.phash(image))

    # Load JSON and get stored phash
    with open(json_path, "r") as f:
        nft_dict = json.load(f)
    stored_phash = nft_dict[str(nft_id)]["phash"]

    print(f"Computed pHash: {computed_phash}")
    print(f"Stored pHash:   {stored_phash}")

    if computed_phash == stored_phash:
        print("✅ Image and JSON pHash match!")
        return True
    else:
        print("❌ Image and JSON pHash DO NOT match!")
        return False

# Example usage:
# verify_image_phash("1234.png", "nft_master_phash_dict.json", 1234)