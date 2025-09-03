import dropbox

def upload_file_dropbox(token: str, file_bytes: bytes, filename: str):
    dbx = dropbox.Dropbox(token)
    path = f"/{filename}"
    dbx.files_upload(file_bytes, path, mode=dropbox.files.WriteMode.overwrite)
    return path

def list_files_dropbox(token: str):
    dbx = dropbox.Dropbox(token)
    result = dbx.files_list_folder("", recursive=True)
    items = []
    for entry in result.entries:
        items.append({
            "name": entry.name,
            "path": entry.path_display,
            "is_folder": isinstance(entry, dropbox.files.FolderMetadata),
            "size": getattr(entry, "size", 0)
        })
    return items

def ensure_folder_exists(token: str, folder_path: str):
    """
    Create folder in Dropbox if it doesn't exist
    """
    dbx = dropbox.Dropbox(token)
    try:
        dbx.files_get_metadata(folder_path)  # check if folder exists
    except dropbox.exceptions.ApiError as e:
        if isinstance(e.error, dropbox.files.GetMetadataError):
            # create folder if missing
            dbx.files_create_folder_v2(folder_path)
        else:
            raise




def normalize_dropbox_path(path: str) -> str:
    """
    Normalize Dropbox path:
    - Convert backslashes to forward slashes
    - Ensure it starts with '/'
    - Remove trailing slash unless it's root
    """
    path = path.replace("\\", "/")
    if not path.startswith("/"):
        path = "/" + path
    if path != "/" and path.endswith("/"):
        path = path.rstrip("/")
    return path


def upload_file_dropbox(token: str, file_bytes: bytes, cloud_path: str):
    """
    Upload a file to Dropbox at the given cloud path.
    """
    dbx = dropbox.Dropbox(token)
    cloud_path = normalize_dropbox_path(cloud_path)

    dbx.files_upload(file_bytes, cloud_path, mode=dropbox.files.WriteMode.overwrite)
    return cloud_path