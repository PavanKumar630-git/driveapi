from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Fix: URL-encoded password
DB_CONN = (
    "mssql+pyodbc://sa:Server%24%23%4054321@61.246.34.128,9042/dropboxfastapi"
    "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

# SQLAlchemy engine
engine = create_engine(DB_CONN, echo=True, future=True)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
