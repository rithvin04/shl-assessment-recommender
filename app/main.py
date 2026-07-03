from fastapi import FastAPI

from app.routes import router
from app.retriever import Retriever

app = FastAPI(
    title="SHL Assessment Recommendation API v2"
)

app.state.retriever = None

app.include_router(router)

@app.get("/")
async def root():
    return {
        "status": "SHL Assessment API is running"
    }