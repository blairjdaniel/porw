import os
import requests
from PIL import Image
import imagehash
from io import BytesIO

def get_profile_image_phash(username: str) -> str:
    """
    Fetches the profile image of a given X (Twitter) username and returns its perceptual hash (pHash).
    """
    bearer_token = os.getenv("X_BEARER_TOKEN")
    if not bearer_token:
        raise ValueError("X_BEARER_TOKEN not set in environment variables.")

    headers = {"Authorization": f"Bearer {bearer_token}"}
    url = f"https://api.twitter.com/2/users/by/username/{username}?user.fields=profile_image_url"

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch profile image: {response.status_code} - {response.text}")

    profile_image_url = response.json()['data']['profile_image_url']

    # Replace _normal with _400x400 to get higher resolution
    profile_image_url = profile_image_url.replace("_normal", "_400x400")

    image_response = requests.get(profile_image_url)
    if image_response.status_code != 200:
        raise Exception(f"Failed to download profile image: {image_response.status_code}")

    img = Image.open(BytesIO(image_response.content))
    hash_val = str(imagehash.phash(img))  # or use .average_hash(), .dhash(), etc.

    return hash_val

def is_matching_nft(phash: str, known_hashes: list, threshold: int = 5) -> bool:
    """
    Compares the given pHash to a list of known NFT hashes and returns True if any are within the threshold.
    """
    for known in known_hashes:
        if imagehash.hex_to_hash(phash) - imagehash.hex_to_hash(known) <= threshold:
            return True
    return False


if __name__ == "__main__":
    phash = get_profile_image_phash("blairjdaniel")
    print(f"Profile image pHash: {phash}")


