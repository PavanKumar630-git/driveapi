from app.utils import auth
from app.utils.dropbox_client import list_dropbox_files
from app.utils.gdrive_client import list_gdrive_files
from app.utils.ftp_client import list_ftp_files

def fetch_files(cloud, emailid, password):
    creds = auth.get_credentials(cloud, emailid, password)

    if cloud.lower() == "dropbox":
        return list_dropbox_files(creds)
    elif cloud.lower() == "gdrive":
        return list_gdrive_files(creds)
    elif cloud.lower() == "ftp":
        return list_ftp_files(creds)
    else:
        raise Exception("Unsupported cloud provider")
