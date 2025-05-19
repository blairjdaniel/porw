import json
import requests
import time
from dotenv import load_dotenv
import os

load_dotenv()

JSON_PATH = "/Users/blairjdaniel/porw/JSON/nft_master_phash_dict.json"
OUTPUT_PATH = "/Users/blairjdaniel/porw/JSON/nft_master_phash_dict.json"
symbol = "rogues"

def fetch_id_to_asset_id():
    all_nfts = []
    offset = 0
    limit = 100
    while True:
        url = f"https://api-mainnet.magiceden.dev/v2/collections/{symbol}/listings?offset={offset}&limit={limit}"
        resp = requests.get(url)
        if resp.status_code == 200:
            nfts = resp.json()
            if not nfts:
                break
            all_nfts.extend(nfts)
            print(f"Fetched {len(nfts)} NFTs (offset {offset})")
            offset += limit
            time.sleep(0.2)
        else:
            print(f"Failed to fetch mints from Magic Eden: {resp.status_code} {resp.text}")
            break
    # Use "tokenMint" as the asset ID
    id_to_asset_id = {str(i): nft.get("tokenMint", "") for i, nft in enumerate(all_nfts)}
    return id_to_asset_id

def main():
    id_to_asset_id = fetch_id_to_asset_id()
    with open(JSON_PATH, "r") as f:
        data = json.load(f)

    for nft_id, info in data.items():
        asset_id = id_to_asset_id.get(nft_id)
        info["asset_id"] = asset_id
        print(f"NFT {nft_id}: asset_id = {asset_id}")
        time.sleep(0.1)

    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()