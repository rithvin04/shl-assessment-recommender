import os
import faiss
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Create vector_db folder if it doesn't exist
os.makedirs("vector_db", exist_ok=True)

# Load dataset
df = pd.read_csv("data/assessments.csv")

# Fill missing values
df = df.fillna("")

# Build richer text for embeddings
df["embedding_text"] = (
    "Assessment Name: " + df["name"].astype(str) + ". " +
    "Description: " + df["description"].astype(str) + ". " +
    "Job Levels: " + df["job_levels_raw"].astype(str) + ". " +
    "Categories: " + df["keys"].astype(str) + ". " +
    "Languages: " + df["languages_raw"].astype(str) + ". " +
    "Duration: " + df["duration_raw"].astype(str) + ". " +
    "Remote Testing: " + df["remote"].astype(str) + ". " +
    "Adaptive: " + df["adaptive"].astype(str)
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Generating embeddings...")

embeddings = model.encode(
    df["embedding_text"].tolist(),
    convert_to_numpy=True,
    show_progress_bar=True
)

embeddings = np.asarray(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

faiss.write_index(index, "vector_db/shl.index")

with open("vector_db/data.pkl", "wb") as f:
    pickle.dump(df, f)

print(f"Indexed {len(df)} assessments successfully.")