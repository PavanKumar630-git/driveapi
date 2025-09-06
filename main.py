from fastapi import FastAPI, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud
from services import dropbox_service, gdrive_service, ftp_service
import os
from concurrent.futures import ThreadPoolExecutor, as_completed


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        

MAX_WORKERS = 10   # number of parallel uploads
DEFAULT_BATCH_SIZE = 50


def process_file(db, email, token, folderpath, cloudfolderpath, file_path):
    """Upload a single file and log into DB."""
    try:
        with open(file_path, "rb") as fp:
            content = fp.read()

        rel_path = os.path.relpath(file_path, folderpath)
        cloud_path = f"{cloudfolderpath}/{rel_path}".replace("\\", "/")

        # upload file to dropbox
        uploaded_path = dropbox_service.upload_file_dropbox(token, content, cloud_path)

        # log in db
        crud.log_uploaded_file(
            db,
            emailid=email,
            cloud="dropbox",
            filelocalpath=file_path,
            cloudpath=uploaded_path,
            filesize=len(content),
            filetype="application/octet-stream",
            status="success",
        )

        return {"file": rel_path, "cloud_path": uploaded_path, "status": "success"}

    except Exception as e:
        return {"file": file_path, "error": str(e), "status": "failed"}


# @app.post("/upload/dropbox/folder")
# def upload_folder_dropbox(
#     email: str = Form(...),
#     token: str = Form(...),
#     folderpath: str = Form(...),         # Local path
#     cloudfolderpath: str = Form(...),    # Cloud destination folder
#     batch_size: int = Form(DEFAULT_BATCH_SIZE),  # 👈 take batch size from payload
#     db: Session = Depends(get_db),
# ):
#     uploaded = []

#     # Ensure remote folder exists
#     dropbox_service.ensure_folder_exists(token, cloudfolderpath)

#     # Collect all files
#     all_files = []
#     for root, _, files in os.walk(folderpath):
#         for f in files:
#             all_files.append(os.path.join(root, f))

#     # Process files in batches
#     for i in range(0, len(all_files), batch_size):
#         batch = all_files[i : i + batch_size]

#         # Parallel upload within batch
#         with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
#             futures = [
#                 executor.submit(process_file, db, email, token, folderpath, cloudfolderpath, f)
#                 for f in batch
#             ]

#             for future in as_completed(futures):
#                 uploaded.append(future.result())

#     return {
#         "total": len(uploaded),
#         "batch_size": batch_size,
#         "uploaded": uploaded,
#     }

@app.post("/upload/dropbox/folder")
def upload_folder_dropbox(
    email: str = Form(...),
    folderpath: str = Form(...),          # Local path
    cloudfolderpath: str = Form(...),     # Cloud destination folder
    batch_size: int = Form(DEFAULT_BATCH_SIZE),  # batch size
    db: Session = Depends(get_db),
):
    uploaded = []

    # 🔹 Get token from DB (InputTableCloud)
    cloud_info = crud.get_cloud_info(db, email, "dropbox")
    if not cloud_info or not cloud_info.tokens:
        return {"error": f"No Dropbox token found for {email}"}

    token = cloud_info.tokens

    # Ensure remote folder exists
    dropbox_service.ensure_folder_exists(token, cloudfolderpath)

    # Collect all files
    all_files = []
    for root, _, files in os.walk(folderpath):
        for f in files:
            all_files.append(os.path.join(root, f))

    # Process files in batches
    for i in range(0, len(all_files), batch_size):
        batch = all_files[i : i + batch_size]

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(process_file, db, email, token, folderpath, cloudfolderpath, f)
                for f in batch
            ]

            for future in as_completed(futures):
                uploaded.append(future.result())

    return {
        "total": len(uploaded),
        "batch_size": batch_size,
        "uploaded": uploaded,
    }

# ----------------- Dropbox -----------------
@app.post("/upload/dropbox")
async def upload_dropbox(email: str = Form(...), token: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    cloud_path = dropbox_service.upload_file_dropbox(token, content, file.filename)

    crud.log_uploaded_file(db, emailid=email, cloud="dropbox", filelocalpath=file.filename,
                           cloudpath=cloud_path, filesize=len(content),
                           filetype=file.content_type, status="success")

    return {"status": "uploaded", "cloud": "dropbox", "path": cloud_path}


@app.get("/list/dropbox")
def list_dropbox(email: str, token: str, db: Session = Depends(get_db)):
    items = dropbox_service.list_files_dropbox(token)
    return {"files": items}


# ----------------- Google Drive -----------------
@app.post("/upload/gdrive")
async def upload_gdrive(email: str = Form(...), credentials_json: str = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info(eval(credentials_json))

    content = await file.read()
    file_id = gdrive_service.upload_file_gdrive(creds, content, file.filename, file.content_type)

    crud.log_uploaded_file(db, emailid=email, cloud="gdrive", filelocalpath=file.filename,
                           cloudpath=file_id, filesize=len(content),
                           filetype=file.content_type, status="success")

    return {"status": "uploaded", "cloud": "gdrive", "file_id": file_id}


@app.get("/list/gdrive")
def list_gdrive(email: str, credentials_json: str, db: Session = Depends(get_db)):
    from google.oauth2.credentials import Credentials
    creds = Credentials.from_authorized_user_info(eval(credentials_json))
    items = gdrive_service.list_files_gdrive(creds)
    return {"files": items}


# ----------------- FTP -----------------
@app.post("/upload/ftp")
async def upload_ftp(email: str = Form(...), host: str = Form(...), user: str = Form(...), password: str = Form(...),
                     file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = await file.read()
    filename = ftp_service.upload_file_ftp(host, user, password, content, file.filename)

    crud.log_uploaded_file(db, emailid=email, cloud="ftp", filelocalpath=file.filename,
                           cloudpath=filename, filesize=len(content),
                           filetype=file.content_type, status="success")

    return {"status": "uploaded", "cloud": "ftp", "filename": filename}


@app.get("/list/ftp")
def list_ftp(email: str, host: str, user: str, password: str, db: Session = Depends(get_db)):
    files = ftp_service.list_files_ftp(host, user, password)
    return {"files": files}
