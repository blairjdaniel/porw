import os
import json
from dotenv import load_dotenv
from image_hash import extract_image_urls_from_ipfs_metadata, hash_ipfs_images, has_specific_desired_traits
from get_profile_image_hash import get_banner_image_phash

load_dotenv()

USERS = ["user1", "user2", "user3"]  # Replace with your X usernames
IPFS_URL = "https://bafybeiforspityxr37tfzupdvjxeszazs76qtv7ecbrfqo6pqwqcghqz6u.ipfs.w3s.link"
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

# Only get image URLs that match the specific traits (or use has_desired_traits for all)
filtered_urls = extract_image_urls_from_ipfs_metadata(
    IPFS_URL, max_items=6969, trait_filter=has_specific_desired_traits
)
nft_hashes = hash_ipfs_images(filtered_urls)

results = {}

for username in USERS:
    print(f"Checking banner for {username}...")
    banner_phash = get_banner_image_phash(username, BEARER_TOKEN)
    user_result = {
        "banner_phash": banner_phash,
        "match": False,
        "match_index": None
    }
    if banner_phash in nft_hashes:
        match_index = nft_hashes.index(banner_phash)
        print(f"Matching NFT found for {username} at index {match_index} (hash: {banner_phash})")
        user_result["match"] = True
        user_result["match_index"] = match_index
    else:
        print(f"No matching NFT found for {username}")
    results[username] = user_result

# Save all results to JSON
with open("banner_phash_results.json", "w") as f:
    json.dump(results, f, indent=2)