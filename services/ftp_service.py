from ftplib import FTP
import io

def upload_file_ftp(host: str, user: str, password: str, file_bytes: bytes, filename: str):
    ftp = FTP(host)
    ftp.login(user=user, passwd=password)
    ftp.storbinary(f"STOR {filename}", io.BytesIO(file_bytes))
    ftp.quit()
    return filename

def list_files_ftp(host: str, user: str, password: str):
    ftp = FTP(host)
    ftp.login(user=user, passwd=password)
    files = []
    ftp.retrlines("LIST", files.append)
    ftp.quit()
    return files
