from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.fetcher import fetch_files

router = APIRouter()

class FetchRequest(BaseModel):
    cloud: str
    emailid: str
    password: str

@router.post("/")
def fetch_api(req: FetchRequest):
    try:
        return fetch_files(req.cloud, req.emailid, req.password)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
