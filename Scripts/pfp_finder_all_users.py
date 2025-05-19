import os
import json
from datetime import datetime

NFT_MASTER_PATH = "/Users/blairjdaniel/porw/JSON/nft_master_phash_dict.json"
CACHE_PATH = "/Users/blairjdaniel/porw/JSON/pfp_daily_cache.json"
RESULTS_PATH = "/Users/blairjdaniel/porw/JSON/pfp_daily_results.json"

def proxy_get_x_pfp_phash(x_account):
    # TODO: Replace with real X API call
    # For now, proxy to the NFT's phash (simulate)
    return "COLLECTION_PHASH"  # <-- Replace with actual logic

def proxy_get_discord_pfp_phash(discord_account):
    # TODO: Replace with real Discord API call
    return "COLLECTION_PHASH"  # <-- Replace with actual logic

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_PATH, "w") as f:
        json.dump(cache, f, indent=2)

def main():
    with open(NFT_MASTER_PATH, "r") as f:
        nft_dict = json.load(f)

    cache = load_cache()
    results = []

    for nft_id, info in nft_dict.items():
        phash = info.get("phash")
        x_account = info.get("x_account")
        discord_account = info.get("discord_account")

        # --- X PFP CHECK ---
        x_pfp_result = None
        if x_account and x_account != "new_twitter_handle":
            username = x_account.lstrip("@")
            current_x_phash = proxy_get_x_pfp_phash(username)
            prev_x_phash = cache.get(f"x_{username}")
            if current_x_phash == prev_x_phash:
                x_pfp_result = cache.get(f"x_{username}_result")
            else:
                x_pfp_result = (current_x_phash == phash)
                cache[f"x_{username}"] = current_x_phash
                cache[f"x_{username}_result"] = x_pfp_result

        # --- DISCORD PFP CHECK ---
        discord_pfp_result = None
        if discord_account and discord_account != "new_discord_handle":
            current_discord_phash = proxy_get_discord_pfp_phash(discord_account)
            prev_discord_phash = cache.get(f"discord_{discord_account}")
            if current_discord_phash == prev_discord_phash:
                discord_pfp_result = cache.get(f"discord_{discord_account}_result")
            else:
                discord_pfp_result = (current_discord_phash == phash)
                cache[f"discord_{discord_account}"] = current_discord_phash
                cache[f"discord_{discord_account}_result"] = discord_pfp_result

        results.append({
            "nft_id": nft_id,
            "x_account": x_account,
            "discord_account": discord_account,
            "pfp_x": bool(x_pfp_result) if x_pfp_result is not None else None,
            "pfp_discord": bool(discord_pfp_result) if discord_pfp_result is not None else None,
        })

    save_cache(cache)
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Daily PFP check complete at {datetime.now()}")

if __name__ == "__main__":
    main()