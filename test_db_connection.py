"""
Test PostgreSQL Database Connection
==================================

Simple script to test if we can connect to PostgreSQL.
"""

import psycopg2
from db_config import DB_CONFIG

def test_connection():
    """Test database connection"""
    try:
        print("Attempting to connect to PostgreSQL...")
        
        # Try to connect
        conn = psycopg2.connect(**DB_CONFIG)
        print("SUCCESS: Connected to PostgreSQL!")
        
        # Get server info
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"PostgreSQL Version: {version[0][:50]}...")
        
        # Test a simple query
        cur.execute("SELECT current_database();")
        db_name = cur.fetchone()
        print(f"Connected to database: {db_name[0]}")
        
        cur.close()
        conn.close()
        print("Connection test completed successfully!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"CONNECTION ERROR: {e}")
        print("\nTroubleshooting tips:")
        print("1. Make sure PostgreSQL is running")
        print("2. Check if the password in db_config.py is correct")
        print("3. Verify the database 'learning_python' exists")
        return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("PostgreSQL Connection Test")
    print("=" * 30)
    test_connection()
