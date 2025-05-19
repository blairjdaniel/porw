import json
import requests
from PIL import Image
from io import BytesIO
import imagehash

IPFS_URL = "https://bafybeife5uclllzgwhy3bchirm556zrsty22dxx7zkzuihqc6ap643yphq.ipfs.dweb.link"
OUTPUT_JSON = "nft_master_phash_list.json"
START_ID = 0
END_ID = 6969  # Adjust as needed

master_list = []

for nft_id in range(START_ID, END_ID):
    image_url = f"{IPFS_URL}/{nft_id}.png"
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            phash = str(imagehash.phash(image))
            master_list.append({"nft_id": nft_id, "phash": phash})
            print(f"Processed NFT {nft_id}: pHash={phash}")
        else:
            print(f"No image for NFT {nft_id} (status {response.status_code})")
    except Exception as e:
        print(f"Error processing NFT {nft_id}: {e}")

with open(OUTPUT_JSON, "w") as f:
    json.dump(master_list, f, indent=2)

print(f"Done! Results saved to {OUTPUT_JSON}")