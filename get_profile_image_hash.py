
from image_hash import extract_image_urls_from_ipfs_metadata, hash_ipfs_images
import requests
import imagehash
from PIL import Image
from io import BytesIO

# Fetch profile image and compute pHash
def get_profile_image_phash(username, bearer_token):
    headers = {
        "Authorization": f"Bearer {bearer_token}"
    }
    url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=profile_image_url"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    image_url = data["data"]["profile_image_url"].replace("_normal", "")

    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    return str(imagehash.phash(image))

# Match against NFT collection
def is_matching_nft(phash, ipfs_base_url, max_items=100):
    nft_image_urls = extract_image_urls_from_ipfs_metadata(ipfs_base_url, max_items)
    nft_hashes = hash_ipfs_images(nft_image_urls)
    return phash in nft_hashes
