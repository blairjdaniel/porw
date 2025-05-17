import imagehash
from PIL import Image
from io import BytesIO
import requests
import json

PROFILE_PHASH = "b1cf869938636c96"
IPFS_IMAGE_BASE = "https://bafybeife5uclllzgwhy3bchirm556zrsty22dxx7zkzuihqc6ap643yphq.ipfs.w3s.link"

# Only check images 4000–4099 (adjust as needed)
START_IDX = 4000
END_IDX = 4100  # Python range is exclusive, so this checks 4000–4099

print(f"Using hardcoded profile image pHash: {PROFILE_PHASH}")

image_urls = [f"{IPFS_IMAGE_BASE}/{i}.png" for i in range(START_IDX, END_IDX)]

result = {
    "profile_phash": PROFILE_PHASH,
    "match": False,
    "match_index": None
}


for idx, url in zip(range(START_IDX, END_IDX), image_urls):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            hash_val = imagehash.phash(image)
            hash_str = str(hash_val)
            distance = imagehash.hex_to_hash(PROFILE_PHASH) - hash_val
            print(f"Checked image {idx}: hash={hash_str} (distance={distance})")
            if distance <= 2:  # Allow up to 2 bits difference
                print(f"Fuzzy match found at index {idx} (hash: {hash_str}, distance: {distance})")
                result["match"] = True
                result["match_index"] = idx
                result["distance"] = distance
                break
        else:
            print(f"Failed to fetch image {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Failed to process image {url}: {e}")

if not result["match"]:
    print("No matching NFT found.")

with open("pfp_phash_results_image_only.json", "w") as f:
    json.dump(result, f, indent=2)