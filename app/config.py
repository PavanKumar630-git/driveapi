import os

class Settings:
    # Example SQL Server connection string
    # Update SERVER, DATABASE, USERNAME, PASSWORD
    DB_CONNECTION_STRING = os.getenv(
        "DB_CONNECTION_STRING",
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=61.246.34.128"
        "DATABASE=dropboxfastapi;"
        "UID=sa;"
        "PWD=Server$#@54321;"
    )

settings = Settings()
