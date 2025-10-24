"""
PostgreSQL Database Setup Script
==============================

This script helps you connect to PostgreSQL and create a database for your Learning_Python project.
"""

import psycopg2
from psycopg2 import sql
import sys

def test_connection():
    """Test connection to PostgreSQL server"""
    try:
        # Try to connect to the default 'postgres' database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password=input("Enter PostgreSQL password: ")
        )
        
        print("Successfully connected to PostgreSQL!")
        
        # Get server version
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"PostgreSQL Version: {version[0]}")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error connecting to PostgreSQL: {e}")
        return False

def create_database():
    """Create a database for the Learning_Python project"""
    try:
        # Connect to postgres database to create new database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="postgres",
            user="postgres",
            password=input("Enter PostgreSQL password: ")
        )
        
        conn.autocommit = True
        cur = conn.cursor()
        
        # Create database
        db_name = "learning_python"
        cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name)))
        print(f"Database '{db_name}' created successfully!")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        if "already exists" in str(e):
            print(f"Database 'learning_python' already exists")
            return True
        else:
            print(f"Error creating database: {e}")
            return False

def create_tables():
    """Create tables for calculator history and user data"""
    try:
        # Connect to our new database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="learning_python",
            user="postgres",
            password=input("Enter PostgreSQL password: ")
        )
        
        cur = conn.cursor()
        
        # Create calculator_history table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS calculator_history (
                id SERIAL PRIMARY KEY,
                expression VARCHAR(255) NOT NULL,
                result VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create users table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        print("Tables created successfully!")
        
        # Show tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public';
        """)
        tables = cur.fetchall()
        print(f"Available tables: {[table[0] for table in tables]}")
        
        cur.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        return False

def main():
    """Main function to set up the database"""
    print("PostgreSQL Database Setup for Learning_Python Project")
    print("=" * 60)
    
    # Test connection
    if not test_connection():
        print("Cannot proceed without database connection")
        sys.exit(1)
    
    # Create database
    if not create_database():
        print("Cannot create database")
        sys.exit(1)
    
    # Create tables
    if not create_tables():
        print("Cannot create tables")
        sys.exit(1)
    
    print("\nDatabase setup completed successfully!")
    print("You can now use this database in your Python applications")

if __name__ == "__main__":
    main()
