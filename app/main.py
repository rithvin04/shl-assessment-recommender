from fastapi import FastAPI

from app.routes import router
from app.retriever import Retriever

app = FastAPI(
    title="SHL Assessment Recommendation API"
)

@app.on_event("startup")
async def startup_event():
    print("Loading Retriever...")
    app.state.retriever = Retriever()
    print("Retriever Loaded Successfully.")

app.include_router(router)

@app.get("/")
async def root():
    return {
        "status": "SHL Assessment API is running"
    }