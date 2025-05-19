import json
import requests
from PIL import Image
from io import BytesIO
import imagehash

IPFS_URL = "https://bafybeife5uclllzgwhy3bchirm556zrsty22dxx7zkzuihqc6ap643yphq.ipfs.w3s.link"
METADATA_IPFS_URL = "https://bafybeiforspityxr37tfzupdvjxeszazs76qtv7ecbrfqo6pqwqcghqz6u.ipfs.w3s.link"
OUTPUT_JSON = "nft_master_phash_list.json"
START_ID = 0
END_ID = 6969  # Adjust as needed

master_list = []

for nft_id in range(START_ID, END_ID):
    image_url = f"{IPFS_URL}/{nft_id}.png"
    metadata_url = f"{METADATA_IPFS_URL}/{nft_id}.json"
    entry = {"nft_id": nft_id}
    try:
        # Get image and compute phash
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            phash = str(imagehash.phash(image))
            entry["phash"] = phash
            print(f"Processed NFT {nft_id}: pHash={phash}")
        else:
            print(f"No image for NFT {nft_id} (status {response.status_code})")
            entry["phash"] = None
    except Exception as e:
        print(f"Error processing NFT {nft_id} image: {e}")
        entry["phash"] = None

    try:
        # Get metadata
        meta_response = requests.get(metadata_url)
        if meta_response.status_code == 200:
            metadata = meta_response.json()
            entry["metadata"] = metadata
        else:
            print(f"No metadata for NFT {nft_id} (status {meta_response.status_code})")
            entry["metadata"] = None
    except Exception as e:
        print(f"Error processing NFT {nft_id} metadata: {e}")
        entry["metadata"] = None

    master_list.append(entry)

with open(OUTPUT_JSON, "w") as f:
    json.dump(master_list, f, indent=2)

print(f"Done! Results saved to {OUTPUT_JSON}")