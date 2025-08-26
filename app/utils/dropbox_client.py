import os
import dropbox

def upload_to_dropbox(creds, localfolder, uploadfolder):
    dbx = dropbox.Dropbox(creds["access_token"])
    for root, _, files in os.walk(localfolder):
        for f in files:
            local_path = os.path.join(root, f)
            cloud_path = f"{uploadfolder}/{f}"
            with open(local_path, "rb") as file_obj:
                dbx.files_upload(file_obj.read(), cloud_path, mode=dropbox.files.WriteMode.overwrite)
            print(f"[Dropbox] Uploaded {local_path} -> {cloud_path}")

def list_dropbox_files(creds):
    dbx = dropbox.Dropbox(creds["access_token"])
    results = []

    def walk_folder(path=""):
        res = dbx.files_list_folder(path)
        for entry in res.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                results.append({
                    "name": entry.name,
                    "size": entry.size,
                    "is_folder": False,
                    "cloud": "dropbox",
                    "parent_path": path,
                    "client_modified": entry.client_modified.isoformat(),
                    "server_modified": entry.server_modified.isoformat(),
                })
            elif isinstance(entry, dropbox.files.FolderMetadata):
                results.append({
                    "name": entry.name,
                    "size": 0,
                    "is_folder": True,
                    "cloud": "dropbox",
                    "parent_path": path
                })
                walk_folder(entry.path_lower)

    walk_folder("")
    return results
