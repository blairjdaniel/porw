import json

input_file = "list.txt"
output_file = "nft_wallets.json"

nft_list = []
with open(input_file, "r") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("//"):
            continue
        # Split on whitespace, take first two columns
        parts = line.split()
        if len(parts) >= 2:
            nft_id = int(parts[0])
            wallet = parts[1]
            nft_list.append({
                "nft_id": nft_id,
                "wallet": wallet
            })

with open(output_file, "w") as f:
    json.dump(nft_list, f, indent=2)

print(f"Saved {len(nft_list)} entries to {output_file}")