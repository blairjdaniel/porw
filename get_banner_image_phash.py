import os
from image_hash import extract_image_urls_from_ipfs_metadata, hash_ipfs_images, has_specific_desired_traits
from get_profile_image_hash import get_banner_image_phash  # You need to implement this
from dotenv import load_dotenv
import json

load_dotenv()

# Constants
USERNAME = "your_x_username"
BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
IPFS_URL = "https://bafybeiforspityxr37tfzupdvjxeszazs76qtv7ecbrfqo6pqwqcghqz6u.ipfs.w3s.link"

# Get the banner image pHash
BANNER_PHASH = get_banner_image_phash(USERNAME, BEARER_TOKEN)
print(f"Using banner image pHash: {BANNER_PHASH}")

# Only get image URLs that match the specific traits (or all, if you want)
filtered_urls = extract_image_urls_from_ipfs_metadata(
    IPFS_URL, max_items=6969, trait_filter=has_specific_desired_traits
)
# Hash the filtered images
nft_hashes = hash_ipfs_images(filtered_urls)

result = {
    "banner_phash": BANNER_PHASH,
    "match": False,
    "match_index": None
}
# Check for match and report
if BANNER_PHASH in nft_hashes:
    match_index = nft_hashes.index(BANNER_PHASH)
    print(f"Matching NFT found at index {match_index} (hash: {BANNER_PHASH})")
    result["match"] = True
    result["match_index"] = match_index
else:
    print("No matching NFT found.")

# Save result to JSON file
with open("banner_phash_results.json", "w") as f:
    json.dump(result, f, indent=2)