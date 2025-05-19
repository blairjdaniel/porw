import json
import os

IMMUTABLE_KEYS = {"nft_id", "phash"}

def update_nft_entry(entry, updates):
    for key, value in updates.items():
        if key in IMMUTABLE_KEYS:
            continue  # Skip immutable fields
        entry[key] = value

# Load the JSON file
json_path = "/Users/blairjdaniel/porw/JSON/nft_wallets.json"
with open(json_path, "r") as f:
    nft_list = json.load(f)

# Example: update wallet and add x_account for nft_id 5759
for entry in nft_list:
    if entry["nft_id"] == 5759:
        update_nft_entry(entry, {
            "wallet": "NEW_WALLET_ADDRESS",
            "x_account": "new_twitter_handle"
        })

# Save the updated JSON file
with open(json_path, "w") as f:
    json.dump(nft_list, f, indent=2)

print("Update complete. Immutable fields were not changed.")