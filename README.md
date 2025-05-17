# porw
RoguesNFT Engagement Program
## How to Use `pfp_blair.py`

This script checks a block of RoguesNFT images on IPFS to see if any match a given profile image's perceptual hash (pHash).
My rogue is 4028.

### Prerequisites

- Python 3.8+
- Install dependencies:
  ```
  pip install pillow imagehash requests
  ```

### Usage

1. **Edit the script if needed:**
   - Set `PROFILE_PHASH` to the pHash of the profile image you want to match.
   - Adjust `START_IDX` and `END_IDX` to the range of image IDs you want to check (e.g., 4000–4100).

2. **Run the script:**
   ```
   python pfp_blair.py
   ```

3. **Output:**
   - The script will print the hash and match status for each image in the range.
   - If a match (or close match) is found, it will print the matching index and save the result to `pfp_phash_results_image_only.json`.

### Notes

- The script uses perceptual hashing, so it can detect visually similar images even if they are not byte-for-byte identical.
- You can change the allowed "distance" for fuzzy matches by editing the `distance <= 2` line in the script.