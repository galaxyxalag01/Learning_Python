"""
Create Database Tables for Learning_Python Project
=================================================

This script creates the necessary tables for the calculator application.
"""

import psycopg2
from db_config import DB_CONFIG

def create_tables():
    """Create tables for the calculator application"""
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        
        print("Creating tables...")
        
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
        
        # Create calculator_sessions table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS calculator_sessions (
                id SERIAL PRIMARY KEY,
                session_id VARCHAR(100) UNIQUE NOT NULL,
                total_calculations INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        conn.commit()
        print("Tables created successfully!")
        
        # Show all tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        print(f"Available tables: {[table[0] for table in tables]}")
        
        cur.close()
        conn.close()
        print("Database setup completed!")
        return True
        
    except psycopg2.Error as e:
        print(f"Error creating tables: {e}")
        return False

if __name__ == "__main__":
    print("Setting up database tables...")
    print("=" * 40)
    create_tables()
