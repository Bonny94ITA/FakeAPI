from fastapi import FastAPI
from app.routes.endpoints import router
from app.routes.reports import router_2

app = FastAPI(title="Fake API from JSON")

app.include_router(router)
app.include_router(router_2)