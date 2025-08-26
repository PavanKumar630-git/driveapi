import os
from app.utils import auth
from app.utils.dropbox_client import upload_to_dropbox
from app.utils.gdrive_client import upload_to_gdrive
from app.utils.ftp_client import upload_to_ftp

def upload_files(cloud, emailid, password, localfolder, uploadfolder):
    creds = auth.get_credentials(cloud, emailid, password)

    if cloud.lower() == "dropbox":
        upload_to_dropbox(creds, localfolder, uploadfolder)
    elif cloud.lower() == "gdrive":
        upload_to_gdrive(creds, localfolder, uploadfolder)
    elif cloud.lower() == "ftp":
        upload_to_ftp(creds, localfolder, uploadfolder)
    else:
        raise Exception("Unsupported cloud provider")

    return {"status": "success", "cloud": cloud, "uploaded_from": localfolder, "uploaded_to": uploadfolder}
