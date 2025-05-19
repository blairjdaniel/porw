import json
import os

# Example variable definitions (replace with your actual data)
x_account = "example_x_account"
profile_phash = "example_profile_phash"
nft_id = "example_nft_id"
nft_phash = "example_nft_phash"
match = True
entry = {
    "wallet": "example_wallet",
    "discord_account": "example_discord"
}

result = {
    "x_account": x_account,
    "profile_phash": profile_phash,
    "nft_id": nft_id,
    "phash": nft_phash,
    "match": match,
    "wallet": entry.get("wallet"),
    "discord_account": entry.get("discord_account")
}

json_path = "nft_master_phash_dict.json"

# Load existing data or start a new dict
if os.path.exists(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
else:
    data = {}

# Use nft_id as the key (make sure it's a string for consistency)
data[str(nft_id)] = result

# Save back to file
with open(json_path, "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved entry for nft_id {nft_id} to {json_path}")