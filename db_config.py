"""
Database Configuration for Learning_Python Project
=================================================

This file contains database connection settings.
Update the password with your PostgreSQL password.
"""

# Database connection settings
DB_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'learning_python',
    'user': 'postgres',
    'password': 'galaxy'  # Replace with your actual PostgreSQL password
}

# Connection string for easy use
CONNECTION_STRING = f"host={DB_CONFIG['host']} port={DB_CONFIG['port']} dbname={DB_CONFIG['database']} user={DB_CONFIG['user']} password={DB_CONFIG['password']}"
