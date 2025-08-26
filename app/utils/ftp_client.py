import os

def upload_to_ftp(creds, localfolder, uploadfolder):
    for root, _, files in os.walk(localfolder):
        for f in files:
            print(f"[FTP] Upload {os.path.join(root, f)} -> {uploadfolder}/{f}")

def list_ftp_files(creds):
    return [{"name": "ftp_file.txt", "size": 789, "is_folder": False, "cloud": "ftp"}]
