from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

def upload_file_gdrive(credentials, file_bytes: bytes, filename: str, mimetype: str):
    service = build("drive", "v3", credentials=credentials)
    media = MediaIoBaseUpload(io.BytesIO(file_bytes), mimetype=mimetype, resumable=True)
    file_metadata = {"name": filename}
    file = service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def list_files_gdrive(credentials):
    service = build("drive", "v3", credentials=credentials)
    results = service.files().list(pageSize=100, fields="files(id, name, mimeType, modifiedTime, size)").execute()
    return results.get("files", [])
