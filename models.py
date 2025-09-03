from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.sql import func
from database import Base


class InputTableCloud(Base):
    __tablename__ = "InputTableCloud"

    id = Column(Integer, primary_key=True, index=True)
    userid = Column(String(100))
    emailid = Column(String(255), index=True)
    password = Column(String(255), nullable=True)
    tokens = Column(Text, nullable=True)
    credentialjson = Column(Text, nullable=True)
    cloud = Column(String(50))
    created_at = Column(DateTime, server_default=func.now())


class OutputFolderStructureTable(Base):
    __tablename__ = "OutputFolderStructureTable"

    id = Column(Integer, primary_key=True, index=True)
    emailid = Column(String(255), index=True)
    name = Column(String(255))
    size = Column(Integer, default=0)
    client_modified = Column(DateTime, nullable=True)
    server_modified = Column(DateTime, nullable=True)
    is_folder = Column(Boolean, default=False)
    parent_path = Column(String(500), nullable=True)
    last_seen = Column(DateTime, server_default=func.now())
    cloud = Column(String(50))


class UploadedDataTable(Base):
    __tablename__ = "UploadedDataTable"

    id = Column(Integer, primary_key=True, index=True)
    emailid = Column(String(255), index=True)
    cloud = Column(String(50))
    filelocalpath = Column(String(500))
    cloudpath = Column(String(500))
    filesize = Column(Integer)
    filetype = Column(String(100))
    uploadedstatus = Column(String(50))
    uploadtimestamp = Column(DateTime, server_default=func.now())
