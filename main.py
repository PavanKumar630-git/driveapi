from fastapi import FastAPI
from app.routes import upload, fetch

app = FastAPI(title="Cloud Uploader API")

# include routers
app.include_router(upload.router, prefix="/upload", tags=["upload"])
app.include_router(fetch.router, prefix="/fetch", tags=["fetch"])
