# -*- coding: utf-8 -*-
"""
Created on Thu Sep  4 00:31:37 2025

@author: Subbu
"""

import pyodbc

try:
    conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=61.246.34.128,9042;"   # IP with port
        "DATABASE=PTS_B2B_TEST;"
        "UID=sa;"
        "PWD=Server$#@54321;"
        "TrustServerCertificate=yes;"
    )

    # connect
    connection = pyodbc.connect(conn_str, timeout=10)
    cursor = connection.cursor()

    print("✅ Connected to SQL Server!")

    # test query
    cursor.execute("SELECT TOP 5 name FROM sys.tables")
    for row in cursor.fetchall():
        print(row)

    cursor.close()
    connection.close()

except Exception as e:
    print("❌ Connection failed:", e)
