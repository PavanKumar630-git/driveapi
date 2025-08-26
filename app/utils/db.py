from sqlalchemy import create_engine

DB_CONN = "mssql+pyodbc://sa:Server$#@54321@61.246.34.128/dropboxfastapi?driver=ODBC+Driver+17+for+SQL+Server"
engine = create_engine(DB_CONN)
