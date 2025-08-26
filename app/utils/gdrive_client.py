import os

def upload_to_gdrive(creds, localfolder, uploadfolder):
    for root, _, files in os.walk(localfolder):
        for f in files:
            print(f"[GDrive] Upload {os.path.join(root, f)} -> {uploadfolder}/{f}")

def list_gdrive_files(creds):
    return [{"name": "gdrive_file.txt", "size": 456, "is_folder": False, "cloud": "gdrive"}]
