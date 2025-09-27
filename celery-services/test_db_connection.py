#!/usr/bin/env python3
"""
Simple script to test direct database connection and query the task_logs table
"""
import pyodbc
from datetime import datetime

def test_connection():
    # Connection parameters
    server = 'localhost'
    port = '1433'
    database = 'master'
    username = 'sa'
    password = 'YourStrong@Passw0rd'
    
    connection_string = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={server},{port};DATABASE={database};UID={username};PWD={password};TrustServerCertificate=yes'
    
    try:
        print("Attempting to connect to SQL Server...")
        conn = pyodbc.connect(connection_string)
        print("✅ Connection successful!")
        
        cursor = conn.cursor()
        
        # Check if table exists and query records
        cursor.execute("""
            SELECT COUNT(*) as count FROM task_logs
        """)
        count = cursor.fetchone()[0]
        print(f"📊 Total records in task_logs: {count}")
        
        # Get recent records
        cursor.execute("""
            SELECT TOP 10 id, task_value, executed_at, status, metadata 
            FROM task_logs 
            ORDER BY executed_at DESC
        """)
        
        records = cursor.fetchall()
        print("\n📋 Recent task logs:")
        print("-" * 80)
        for record in records:
            print(f"ID: {record[0]:3d} | Value: {record[1]:15s} | Time: {record[2]} | Status: {record[3]}")
        
        # Insert a test record from outside
        cursor.execute("""
            INSERT INTO task_logs (task_value, executed_at, status, metadata)
            VALUES (?, ?, ?, ?)
        """, (
            'direct_test',
            datetime.now(),
            'manual_test',
            '{"source": "direct_connection", "test": true}'
        ))
        conn.commit()
        print("\n✅ Successfully inserted test record from direct connection")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    test_connection()
