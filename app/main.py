from fastapi import FastAPI
from app.routes import upload, fetch

app = FastAPI()

app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(fetch.router, prefix="/fetch", tags=["Fetch"])
