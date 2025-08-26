CREATE TABLE InputTableCloud (
    userid INT IDENTITY(1,1) PRIMARY KEY,
    emailid VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    tokens TEXT NULL,
    credentialjson TEXT NULL
);

CREATE TABLE UploadedDataTable (
    id INT IDENTITY(1,1) PRIMARY KEY,
    filelocalpath VARCHAR(500),
    cloudpath VARCHAR(500),
    cloudtype VARCHAR(50),
    filesize BIGINT,
    filetype VARCHAR(50),
    uploadedstatus VARCHAR(50),
    uploadtimestamp DATETIME DEFAULT GETDATE()
);

CREATE TABLE OutputFolderStructureTable (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name VARCHAR(255),
    size BIGINT,
    client_modified DATETIME NULL,
    server_modified DATETIME NULL,
    is_folder BIT,
    parent_path VARCHAR(500),
    last_seen DATETIME DEFAULT GETDATE(),
    cloud VARCHAR(50)
);
