from sqlalchemy.orm import Session
from models import UploadedDataTable, OutputFolderStructureTable
from datetime import datetime


def log_uploaded_file(db: Session, emailid: str, cloud: str, filelocalpath: str,
                      cloudpath: str, filesize: int, filetype: str, status: str):
    entry = UploadedDataTable(
        emailid=emailid,
        cloud=cloud,
        filelocalpath=filelocalpath,
        cloudpath=cloudpath,
        filesize=filesize,
        filetype=filetype,
        uploadedstatus=status,
        uploadtimestamp=datetime.utcnow()
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def save_folder_structure(db: Session, emailid: str, cloud: str, items: list):
    """
    items = list of dicts with keys: name, size, is_folder, parent_path, client_modified, server_modified
    """
    for it in items:
        entry = OutputFolderStructureTable(
            emailid=emailid,
            name=it.get("name"),
            size=it.get("size", 0),
            is_folder=it.get("is_folder", False),
            parent_path=it.get("parent_path"),
            client_modified=it.get("client_modified"),
            server_modified=it.get("server_modified"),
            last_seen=datetime.utcnow(),
            cloud=cloud
        )
        db.add(entry)
    db.commit()
