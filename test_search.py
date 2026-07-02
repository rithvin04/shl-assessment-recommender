from app.retriever import Retriever

retriever = Retriever()
matches = retriever.df[retriever.df["name"].str.contains("python", case=False, na=False)]
print(matches[["name"]])

query = "Graduate software engineer"

results = retriever.search(query)

for i, item in enumerate(results, start=1):
    print("=" * 80)
    print(f"Rank: {i}")
    print(f"Name: {item['name']}")
    print(f"Duration: {item['duration']}")
    print(f"Remote: {item['remote']}")
    print(f"Adaptive: {item['adaptive']}")
    print(f"Job Levels: {item['job_levels']}")
    print(f"Categories: {item['categories']}")
    print(f"URL: {item['url']}")