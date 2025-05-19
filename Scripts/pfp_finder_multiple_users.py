import os
import json
import requests
from PIL import Image
from io import BytesIO
import imagehash

NFT_WALLETS_PATH = "/Users/blairjdaniel/porw/JSON/nft_wallets.json"
FUZZY_THRESHOLD = 2
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")  # Or paste your token here as a string

def get_profile_image_url(username, bearer_token):
    url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=profile_image_url"
    headers = {"Authorization": f"Bearer {bearer_token}"}
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    data = resp.json()
    return data["data"]["profile_image_url"].replace("_normal", "")

def get_profile_image_phash(username, bearer_token):
    img_url = get_profile_image_url(username, bearer_token)
    img_resp = requests.get(img_url)
    img_resp.raise_for_status()
    img = Image.open(BytesIO(img_resp.content))
    phash = str(imagehash.phash(img))
    return phash

def is_valid_x_account(x_account):
    return x_account and x_account != "new_twitter_handle"

def main():
    with open(NFT_WALLETS_PATH, "r") as f:
        nft_list = json.load(f)

    results = []
    for entry in nft_list:
        x_account = entry.get("x_account", "")
        nft_id = entry.get("nft_id")
        nft_phash = entry.get("phash")
        if not is_valid_x_account(x_account) or not nft_phash:
            continue
        username = x_account.lstrip("@")
        try:
            profile_phash = get_profile_image_phash(username, BEARER_TOKEN)
        except Exception as e:
            print(f"Could not fetch pfp for {username}: {e}")
            continue
        distance = imagehash.hex_to_hash(profile_phash) - imagehash.hex_to_hash(nft_phash)
        match = distance <= FUZZY_THRESHOLD
        result = {
            "nft_id": nft_id,
            "x_account": x_account,
            "profile_phash": profile_phash,
            "nft_phash": nft_phash,
            "distance": distance,
            "match": match,
            "wallet": entry.get("wallet"),
            "discord_account": entry.get("discord_account")
        }
        print(result)
        results.append(result)

    with open("pfp_matches_all_users.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()