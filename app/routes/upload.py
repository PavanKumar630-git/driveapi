from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.uploader import upload_files

router = APIRouter()

class UploadRequest(BaseModel):
    cloud: str
    emailid: str
    password: str
    localfolder: str
    uploadfolder: str

@router.post("/")
def upload_api(req: UploadRequest):
    try:
        return upload_files(req.cloud, req.emailid, req.password, req.localfolder, req.uploadfolder)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
