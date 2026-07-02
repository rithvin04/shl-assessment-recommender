from fastapi import FastAPI

from app.routes import router
from app.retriever import Retriever

app = FastAPI()

retriever = Retriever()

app.state.retriever = retriever

app.include_router(router)