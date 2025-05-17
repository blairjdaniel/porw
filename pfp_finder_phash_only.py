import os
from image_hash import extract_image_urls_from_ipfs_metadata, hash_ipfs_images
from dotenv import load_dotenv
load_dotenv()
import json

# Constants
PROFILE_PHASH = "b1cf869938636c96"
IPFS_URL = "https://bafybeiforspityxr37tfzupdvjxeszazs76qtv7ecbrfqo6pqwqcghqz6u.ipfs.w3s.link"

print(f"Using hardcoded profile image pHash: {PROFILE_PHASH}")

# Fetch NFT image URLs from IPFS that match specific traits
image_urls = extract_image_urls_from_ipfs_metadata(IPFS_URL, max_items=6969)
# Filter URLs by specific traits
filtered_urls = []
for i, url in enumerate(image_urls):
    # You need to fetch the metadata again to check traits, unless you modify extract_image_urls_from_ipfs_metadata to accept a trait filter function
    # For now, assume extract_image_urls_from_ipfs_metadata uses has_specific_desired_traits internally
    filtered_urls.append(url)

# # Only get image URLs that match the specific traits
# filtered_urls = extract_image_urls_from_ipfs_metadata(
#     IPFS_URL, max_items=6969, trait_filter=has_specific_desired_traits
# )
# Hash the filtered images
nft_hashes = hash_ipfs_images(filtered_urls)

result = {
    "profile_phash": PROFILE_PHASH,
    "match": False,
    "match_index": None
}
# Check for match and report
if PROFILE_PHASH in nft_hashes:
    match_index = nft_hashes.index(PROFILE_PHASH)
    print(f"Matching NFT found at index {match_index} (hash: {PROFILE_PHASH})")
else:
    print("No matching NFT found.")

# Save result to JSON file
with open("pfp_phash_results.json", "w") as f:
    json.dump(result, f, indent=2)