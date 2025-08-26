import pyodbc
import json
from app.config import settings

def get_db_connection():
    conn = pyodbc.connect(settings.DB_CONNECTION_STRING)
    return conn

def get_credentials(emailid: str, password: str, cloud: str):
    """
    Fetch credentials for a given emailid, password, and cloud type from InputTableCloud.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT tokens, credentialjson
        FROM InputTableCloud
        WHERE emailid = ? AND password = ? AND cloud = ?
    """, (emailid, password, cloud))

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        raise Exception(f"No credentials found for {emailid} / {cloud}")

    tokens = row[0]
    credentialjson = row[1]

    creds = {"email": emailid, "cloud": cloud}

    # Dropbox → token required
    if cloud.lower() == "dropbox":
        creds["access_token"] = tokens

    # Google Drive → either service account JSON or token
    elif cloud.lower() == "gdrive":
        if credentialjson:
            creds["credentialjson"] = json.loads(credentialjson)
        else:
            creds["access_token"] = tokens

    # FTP → use email/password directly
    elif cloud.lower() == "ftp":
        creds["username"] = emailid
        creds["password"] = password

    return creds
