from fastapi import FastAPI
from app.routes import router
from app.retriever import Retriever

app = FastAPI()

app.include_router(router)


@app.on_event("startup")
async def startup():
    print("Loading retriever...")
    app.state.retriever = Retriever()
    print("Retriever loaded.")