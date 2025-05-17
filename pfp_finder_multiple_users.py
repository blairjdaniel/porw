import os
from get_profile_image_hash import get_profile_image_phash
from image_hash import load_and_hash_images_from_ipfs
from dotenv import load_dotenv
from save_pfp_pHash import load_json, save_json

load_dotenv()

USERS = ["user1", "user2", "user3"]  # Replace with your list of usernames
IPFS_URL = "https://bafybeiforspityxr37tfzupdvjxeszazs76qtv7ecbrfqo6pqwqcghqz6u.ipfs.w3s.link"
PHASH_RECORD = "user_phashes.json"
RESULTS_RECORD = "user_results.json"
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

# Load previous pHashes and results using the helper functions
prev_phashes = load_json(PHASH_RECORD)
results = load_json(RESULTS_RECORD)

for username in USERS:
    print(f"Checking {username}...")
    profile_phash = get_profile_image_phash(username, BEARER_TOKEN)
    if not profile_phash:
        print(f"Could not fetch pHash for {username}")
        continue

    if prev_phashes.get(username) == profile_phash:
        print(f"No change in pHash for {username}, skipping NFT check.")
        # Carry forward previous match result if it exists, else set to None
        prev_result = results.get(username, {})
        results[username] = {
            "profile_phash": profile_phash,
            "match": prev_result.get("match", None),
            "match_index": prev_result.get("match_index", None)
        }
        continue

    print(f"New pHash for {username}: {profile_phash}, running NFT check...")
    nft_hashes = load_and_hash_images_from_ipfs(IPFS_URL, max_items=100)  # Adjust as needed
    if profile_phash in nft_hashes:
        match_index = nft_hashes.index(profile_phash)
        print(f"Matching NFT found for {username} at index {match_index}")
        results[username] = {
            "profile_phash": profile_phash,
            "match": True,
            "match_index": match_index
        }
    else:
        print(f"No matching NFT found for {username}")
        results[username] = {
            "profile_phash": profile_phash,
            "match": False,
            "match_index": None
        }

    # Update stored pHash
    prev_phashes[username] = profile_phash

# Save updated pHashes and results using the helper functions
save_json(PHASH_RECORD, prev_phashes)
save_json(RESULTS_RECORD, results)

STAKED_IDS = {
    "user1": [4028, 123, 456],  # Replace with actual staked IDs for each user
    "user2": [789, 234],
    "user3": []
}

for username in USERS:
    print(f"Checking {username}...")
    profile_phash = get_profile_image_phash(username, BEARER_TOKEN)
    if not profile_phash:
        print(f"Could not fetch pHash for {username}")
        continue

    if prev_phashes.get(username) == profile_phash:
        print(f"No change in pHash for {username}, skipping NFT check.")
        prev_result = results.get(username, {})
        results[username] = {
            "profile_phash": profile_phash,
            "match": prev_result.get("match", None),
            "match_index": prev_result.get("match_index", None)
        }
        continue

    # First, check staked IDs
    staked_ids = STAKED_IDS.get(username, [])
    staked_urls = [f"{IPFS_URL}/{i}.png" for i in staked_ids]
    from image_hash import hash_ipfs_images  # Import here if not already
    staked_hashes = hash_ipfs_images(staked_urls)
    if profile_phash in staked_hashes:
        match_index = staked_ids[staked_hashes.index(profile_phash)]
        print(f"Matching NFT found for {username} in staked IDs at index {match_index}")
        results[username] = {
            "profile_phash": profile_phash,
            "match": True,
            "match_index": match_index
        }
        prev_phashes[username] = profile_phash
        continue  # Skip checking the rest

    # If not found in staked, check the rest (as before)
    print(f"No match in staked IDs, checking full collection for {username}...")
    nft_hashes = load_and_hash_images_from_ipfs(IPFS_URL, max_items=100)  # Adjust as needed
    if profile_phash in nft_hashes:
        match_index = nft_hashes.index(profile_phash)
        print(f"Matching NFT found for {username} at index {match_index}")
        results[username] = {
            "profile_phash": profile_phash,
            "match": True,
            "match_index": match_index
        }
    else:
        print(f"No matching NFT found for {username}")
        results[username] = {
            "profile_phash": profile_phash,
            "match": False,
            "match_index": None
        }

    prev_phashes[username] = profile_phash

# Save updated pHashes and results using the helper functions
save_json(PHASH_RECORD, prev_phashes)
save_json(RESULTS_RECORD, results)