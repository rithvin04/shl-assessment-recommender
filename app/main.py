from fastapi import FastAPI

print("STEP 1: main.py imported")

from app.routes import router

print("STEP 2: routes imported")

app = FastAPI(
    title="SHL Assessment Recommendation API"
)

print("STEP 3: FastAPI created")

app.state.retriever = None

print("STEP 4: retriever set to None")

app.include_router(router)

print("STEP 5: router included")

@app.get("/")
async def root():
    return {
        "status": "SHL Assessment API is running"
    }

print("STEP 6: root route added")