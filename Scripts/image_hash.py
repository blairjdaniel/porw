import os
import requests
import imagehash
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()
ipfs_base_url = os.getenv("IPFS", "https://ipfs.io/ipfs/")

def ipfs_to_http(ipfs_uri):
    """Convert ipfs:// URI to https://ipfs.io/ipfs/ URL."""
    if ipfs_uri.startswith("ipfs://"):
        return ipfs_uri.replace("ipfs://", "https://ipfs.io/ipfs/")
    return ipfs_uri

def extract_image_urls_from_ipfs_metadata(base_url, max_items=6969, trait_filter=None):
    """
    Extract image URLs from IPFS metadata JSONs.
    Optionally filter by a trait_filter function.
    """
    image_urls = []
    for i in range(max_items):
        json_url = f"{base_url}/{i}.json"
        print(f"Checking JSON metadata: {json_url}")
        try:
            response = requests.get(json_url)
            if response.status_code == 200:
                metadata = response.json()
                attributes = metadata.get("attributes", [])
                if trait_filter and not trait_filter(attributes):
                    continue  # Skip NFTs that don't match the trait filter
                image_ipfs = metadata.get("image")
                if image_ipfs:
                    image_urls.append(ipfs_to_http(image_ipfs))
            else:
                break
        except Exception as e:
            print(f"Failed to parse {json_url}: {e}")
            continue
    return image_urls

def hash_ipfs_images(urls):
    """Download images from URLs and compute their perceptual hashes."""
    hashes = []
    for url in urls:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                image = Image.open(BytesIO(response.content))
                hash_val = imagehash.phash(image)
                hashes.append(str(hash_val))
            else:
                print(f"Failed to fetch image {url}: Status {response.status_code}")
        except Exception as e:
            print(f"Failed to hash image {url}: {e}")
    return hashes

def load_and_hash_images_from_ipfs(base_url, max_items=6969, trait_filter=None):
    """
    Extract image URLs (optionally filtered) and return their pHashes.
    """
    image_urls = extract_image_urls_from_ipfs_metadata(base_url, max_items, trait_filter)
    return hash_ipfs_images(image_urls) 