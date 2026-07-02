import json
import pandas as pd
import os

os.makedirs("data", exist_ok=True)

with open("data/shl_catalog_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f, strict=False)

df = pd.DataFrame(data)

print("Shape:", df.shape)
print("\nColumns:")
print(df.columns.tolist())

df.to_csv("data/assessments.csv", index=False)

print("\nSaved successfully!")