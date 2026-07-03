import faiss
import pickle
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

from app.query_analyzer import analyze_query


class Retriever:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            "vector_db/shl.index"
        )

        with open(
            "vector_db/data.pkl",
            "rb"
        ) as f:

            self.df = pickle.load(f)

        print(f"Loaded {len(self.df)} assessments.")
    def search(self, query, top_k=5):

        filters = analyze_query(query)

        candidates = self.df.copy()

        if filters["remote"]:
            candidates = candidates[
                candidates["remote"].str.lower() == "yes"
            ]

        if filters["adaptive"]:
            candidates = candidates[
                candidates["adaptive"].str.lower() == "yes"
            ]

        if filters["job_level"]:
            candidates = candidates[
                candidates["job_levels_raw"]
                .str.lower()
                .str.contains(filters["job_level"], na=False)
            ]

        if candidates.empty:
            candidates = self.df.copy()

        candidate_indices = candidates.index.to_numpy()

        # --- KEYWORD OVERRIDE: catch exact skill/tech mentions ---
        query_lower = query.lower()
        keyword_matches = []

        for idx in candidate_indices:
            row = self.df.iloc[idx]
            name_lower = str(row["name"]).lower()
            clean_name = name_lower.replace("(new)", "").strip()

            if clean_name and clean_name in query_lower:
                keyword_matches.append(idx)

        # --- Semantic search ---
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype(np.float32)

        distances, indices = self.index.search(
            query_embedding,
            min(50, len(self.df))
        )

        semantic_matches = [
            idx for idx in indices[0]
            if idx in candidate_indices and idx not in keyword_matches
        ]

        final_indices = keyword_matches + semantic_matches
        final_indices = final_indices[:top_k]

        recommendations = []
        for idx in final_indices:
            row = self.df.iloc[idx]
            recommendations.append({
                "name": row["name"],
                "description": row["description"],
                "url": row["link"],
                "duration": row["duration_raw"],
                "remote": row["remote"],
                "adaptive": row["adaptive"],
                "job_levels": row["job_levels_raw"],
                "categories": row["keys"]
            })

        return recommendations
    def compare(self, assessment_names):

        results = []

        for name in assessment_names:
            search_name = name.lower().strip()
            match = self.df[
                self.df["name"]
                .str.lower()
                .str.contains(
                    search_name,
                    case=False,
                    regex=False,
                    na=False
                )
            ]
            
            if match.empty:
                results.append({
                    "name": name,
                    "found": False,
                })
                continue

            row = match.iloc[0]

            categories = row["keys"]

            if isinstance(categories, list):
                categories = ", ".join(categories)
            else:
                categories = str(categories)

            description = str(row["description"])

            if "Your use of this assessment product" in description:
                description = description.split(
                    "Your use of this assessment product"
                )[0].strip()

            results.append({
                "name": row["name"],
                "found": True,
                "description": description,
                "url": row["link"],
                "duration": row["duration_raw"],
                "remote": row["remote"],
                "adaptive": row["adaptive"],
                "categories": categories
            })

        return {
            "requested": assessment_names,

            "results": results
        }