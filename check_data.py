import pickle

with open("vector_db/data.pkl", "rb") as f:
    df = pickle.load(f)

print("\nColumns:\n")
print(df.columns.tolist())

print("\nFirst 2 Rows:\n")
print(df.head(2))