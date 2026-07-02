import json

with open("data/shl_catalog_raw.json", "r", encoding="utf-8", errors="replace") as f:
    text = f.read()

print("File length:", len(text))

try:
    data = json.loads(text, strict=False)
    print("Loaded successfully!")
    print(type(data))

    if isinstance(data, list):
        print("Total assessments:", len(data))
        print("\nFirst assessment:")
        print(data[0])

    elif isinstance(data, dict):
        print("Keys:")
        print(data.keys())

except Exception as e:
    print("Error:", e)