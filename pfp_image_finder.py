# ...existing imports...
import imagehash
from PIL import Image
from io import BytesIO
import requests
import json

# Constants
PROFILE_PHASH = "b1cf869938636c96"
IPFS_IMAGE_BASE = "https://bafybeife5uclllzgwhy3bchirm556zrsty22dxx7zkzuihqc6ap643yphq.ipfs.w3s.link"
NUM_IMAGES = 6969  # Adjust as needed

print(f"Using hardcoded profile image pHash: {PROFILE_PHASH}")

# Generate all image URLs
image_urls = [f"{IPFS_IMAGE_BASE}/{i}.png" for i in range(NUM_IMAGES)]

result = {
    "profile_phash": PROFILE_PHASH,
    "match": False,
    "match_index": None
}

for idx, url in enumerate(image_urls):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            hash_val = str(imagehash.phash(image))
            print(f"Checked image {idx}: hash={hash_val} (match={hash_val == PROFILE_PHASH})")
            if hash_val == PROFILE_PHASH:
                print(f"Matching NFT found at index {idx} (hash: {PROFILE_PHASH})")
                result["match"] = True
                result["match_index"] = idx
                break
        else:
            print(f"Failed to fetch image {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Failed to process image {url}: {e}")

if not result["match"]:
    print("No matching NFT found.")

# Save result to JSON file
with open("pfp_phash_results_image_only.json", "w") as f:
    json.dump(result, f, indent=2)