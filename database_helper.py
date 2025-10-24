"""
Database Helper Module for Calculator Applications
=================================================

This module provides functions to interact with the PostgreSQL database
for storing and retrieving calculator history.
"""

import psycopg2
from psycopg2 import sql
from db_config import DB_CONFIG
import json
from datetime import datetime

class CalculatorDB:
    """Database operations for calculator applications"""
    
    def __init__(self):
        self.conn = None
        self.connect()
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            return True
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def save_calculation(self, expression, result, session_id=None):
        """
        Save a calculation to the database
        
        Args:
            expression (str): The mathematical expression
            result (str): The calculated result
            session_id (str): Optional session identifier
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.conn:
                self.connect()
            
            cur = self.conn.cursor()
            
            # Insert calculation into history
            cur.execute("""
                INSERT INTO calculator_history (expression, result)
                VALUES (%s, %s)
                RETURNING id;
            """, (expression, result))
            
            calculation_id = cur.fetchone()[0]
            
            # Update session if provided
            if session_id:
                self.update_session(session_id, calculation_id)
            
            self.conn.commit()
            cur.close()
            return True
            
        except psycopg2.Error as e:
            print(f"Error saving calculation: {e}")
            if self.conn:
                self.conn.rollback()
            return False
    
    def get_calculation_history(self, limit=50):
        """
        Retrieve calculation history from database
        
        Args:
            limit (int): Maximum number of records to return
        
        Returns:
            list: List of calculation records
        """
        try:
            if not self.conn:
                self.connect()
            
            cur = self.conn.cursor()
            
            cur.execute("""
                SELECT id, expression, result, created_at
                FROM calculator_history
                ORDER BY created_at DESC
                LIMIT %s;
            """, (limit,))
            
            history = cur.fetchall()
            cur.close()
            
            return history
            
        except psycopg2.Error as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def create_session(self, session_id):
        """
        Create a new calculator session
        
        Args:
            session_id (str): Unique session identifier
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.conn:
                self.connect()
            
            cur = self.conn.cursor()
            
            cur.execute("""
                INSERT INTO calculator_sessions (session_id)
                VALUES (%s)
                ON CONFLICT (session_id) DO NOTHING;
            """, (session_id,))
            
            self.conn.commit()
            cur.close()
            return True
            
        except psycopg2.Error as e:
            print(f"Error creating session: {e}")
            if self.conn:
                self.conn.rollback()
            return False
    
    def update_session(self, session_id, calculation_id=None):
        """
        Update session statistics
        
        Args:
            session_id (str): Session identifier
            calculation_id (int): Optional calculation ID
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.conn:
                self.connect()
            
            cur = self.conn.cursor()
            
            # Update total calculations and last used timestamp
            cur.execute("""
                UPDATE calculator_sessions
                SET total_calculations = total_calculations + 1,
                    last_used = CURRENT_TIMESTAMP
                WHERE session_id = %s;
            """, (session_id,))
            
            self.conn.commit()
            cur.close()
            return True
            
        except psycopg2.Error as e:
            print(f"Error updating session: {e}")
            if self.conn:
                self.conn.rollback()
            return False
    
    def get_session_stats(self, session_id):
        """
        Get statistics for a session
        
        Args:
            session_id (str): Session identifier
        
        Returns:
            dict: Session statistics
        """
        try:
            if not self.conn:
                self.connect()
            
            cur = self.conn.cursor()
            
            cur.execute("""
                SELECT total_calculations, created_at, last_used
                FROM calculator_sessions
                WHERE session_id = %s;
            """, (session_id,))
            
            result = cur.fetchone()
            cur.close()
            
            if result:
                return {
                    'total_calculations': result[0],
                    'created_at': result[1],
                    'last_used': result[2]
                }
            return None
            
        except psycopg2.Error as e:
            print(f"Error getting session stats: {e}")
            return None
    
    def clear_history(self):
        """
        Clear all calculation history
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not self.conn:
                self.connect()
            
            cur = self.conn.cursor()
            
            cur.execute("DELETE FROM calculator_history;")
            
            self.conn.commit()
            cur.close()
            return True
            
        except psycopg2.Error as e:
            print(f"Error clearing history: {e}")
            if self.conn:
                self.conn.rollback()
            return False

# Convenience functions for easy use
def save_calculation(expression, result, session_id=None):
    """Save a calculation to the database"""
    db = CalculatorDB()
    success = db.save_calculation(expression, result, session_id)
    db.disconnect()
    return success

def get_history(limit=50):
    """Get calculation history"""
    db = CalculatorDB()
    history = db.get_calculation_history(limit)
    db.disconnect()
    return history

def clear_history():
    """Clear all calculation history"""
    db = CalculatorDB()
    success = db.clear_history()
    db.disconnect()
    return success
