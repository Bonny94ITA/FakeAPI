# app/main.py
from fastapi import FastAPI
from app.routes.endpoints import router

app = FastAPI(title="Fake API from JSON")

app.include_router(router)
