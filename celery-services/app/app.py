import os
import pyodbc
from datetime import datetime
import json

def get_db_connection():
    """Get database connection using environment variables or defaults"""
    server = os.getenv('MSSQL_HOST', 'mssqlserver')
    port = os.getenv('MSSQL_PORT', '1433')
    database = os.getenv('MSSQL_DATABASE', 'master')
    username = os.getenv('MSSQL_USER', 'sa')
    password = os.getenv('MSSQL_PASSWORD', 'YourStrong@Passw0rd')
    
    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'
    
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Database connection failed: {e}")
        return None

def create_table_if_not_exists(conn):
    """Create a sample table if it doesn't exist"""
    try:
        cursor = conn.cursor()
        
        # Check if table exists
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='task_logs' AND xtype='U')
            CREATE TABLE task_logs (
                id INT IDENTITY(1,1) PRIMARY KEY,
                task_value NVARCHAR(255),
                executed_at DATETIME,
                status NVARCHAR(50),
                metadata NVARCHAR(MAX)
            )
        """)
        conn.commit()
        print("Table 'task_logs' created or already exists")
        return True
    except Exception as e:
        print(f"Error creating table: {e}")
        return False

def write_task_data(conn, val):
    """Write task execution data to database"""
    try:
        cursor = conn.cursor()
        
        # Insert task execution record
        cursor.execute("""
            INSERT INTO task_logs (task_value, executed_at, status, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            str(val),
            datetime.now(),
            'completed',
            json.dumps({'worker': 'celery', 'version': '1.0'})
        ))
        
        conn.commit()
        
        # Get the inserted record ID
        cursor.execute("SELECT @@IDENTITY")
        record_id = cursor.fetchone()[0]
        
        print(f"Data written to database. Record ID: {record_id}")
        return record_id
        
    except Exception as e:
        print(f"Error writing to database: {e}")
        return None

def run(val):
    print(f"Task executed with value: {val}")
    
    # Connect to database
    conn = get_db_connection()
    if conn is None:
        print("Skipping database operations due to connection failure")
        return val
    
    try:
        # Create table if needed
        if create_table_if_not_exists(conn):
            # Write task data
            record_id = write_task_data(conn, val)
            if record_id:
                print(f"Successfully logged task execution to database (ID: {record_id})")
            else:
                print("Failed to write task data to database")
        
        # Query recent records to verify
        cursor = conn.cursor()
        cursor.execute("SELECT TOP 5 * FROM task_logs ORDER BY executed_at DESC")
        recent_records = cursor.fetchall()
        
        print("Recent task logs:")
        for record in recent_records:
            print(f"  ID: {record[0]}, Value: {record[1]}, Time: {record[2]}, Status: {record[3]}")
            
    except Exception as e:
        print(f"Database operation error: {e}")
    
    finally:
        conn.close()
    
    return val