import os
import json
import requests
from PIL import Image
from io import BytesIO
import imagehash
import time

NFT_WALLETS_PATH = "/Users/blairjdaniel/porw/JSON/nft_wallets.json"
MASTER_PHASH_PATH = "/Users/blairjdaniel/porw/JSON/nft_master_phash_list.json"
CACHE_PATH = "x_banner_phash_cache.json"
FUZZY_THRESHOLD = 2
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

def get_banner_image_url(username, bearer_token):
    url = f"https://api.twitter.com/1.1/users/show.json?screen_name={username}"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    banner_url = data.get("profile_banner_url")
    if not banner_url:
        raise ValueError("No banner image found for user.")
    # Twitter returns a base URL; append '/1500x500' for the full-size banner
    return banner_url + "/1500x500"

def get_banner_image_phash(username, bearer_token):
    img_url = get_banner_image_url(username, bearer_token)
    img_resp = requests.get(img_url)
    img_resp.raise_for_status()
    img = Image.open(BytesIO(img_resp.content))
    phash = str(imagehash.phash(img))
    return phash

def is_valid_x_account(x_account):
    return x_account and x_account != "new_twitter_handle"

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def main():
    with open(NFT_WALLETS_PATH, "r") as f:
        nft_dict = json.load(f)
    with open(MASTER_PHASH_PATH, "r") as f:
        master_phash_list = json.load(f)

    cache = load_cache()
    results = []
    for entry in nft_dict:
        x_account = entry.get("x_account", "")
        if not is_valid_x_account(x_account):
            continue
        username = x_account.lstrip("@")
        try:
            banner_phash = get_banner_image_phash(username, BEARER_TOKEN)
            time.sleep(2)  # Rate limit handling
        except Exception as e:
            print(f"Could not fetch banner for {username}: {e}")
            continue

        # Skip if pHash hasn't changed
        if cache.get(username) == banner_phash:
            print(f"No change in banner for {username}, skipping NFT check.")
            continue

        # Compare to all NFTs in master list
        for nft in master_phash_list:
            nft_id = nft["nft_id"]
            nft_phash = nft["phash"]
            distance = imagehash.hex_to_hash(banner_phash) - imagehash.hex_to_hash(nft_phash)
            match = distance <= FUZZY_THRESHOLD
            if match:
                result = {
                    "x_account": x_account,
                    "banner_phash": banner_phash,
                    "nft_id": nft_id,
                    "nft_phash": nft_phash,
                    "distance": distance,
                    "match": match,
                    "wallet": entry.get("wallet"),
                    "discord_account": entry.get("discord_account")
                }
                print(result)
                results.append(result)

        # Update cache
        cache[username] = banner_phash

    save_cache(cache)

    with open("banner_matches_to_master.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()