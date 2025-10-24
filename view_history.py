"""
View Calculation History from Database
=====================================

Simple script to view and manage calculation history stored in PostgreSQL.
"""

from database_helper import get_history, clear_history
from datetime import datetime

def display_history(limit=20):
    """Display calculation history in a formatted way"""
    print("=" * 60)
    print("CALCULATION HISTORY")
    print("=" * 60)
    
    try:
        history = get_history(limit)
        
        if not history:
            print("No calculation history found.")
            return
        
        print(f"Showing last {len(history)} calculations:\n")
        
        for i, record in enumerate(history, 1):
            calc_id, expression, result, timestamp = record
            time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"{i:2d}. [{time_str}]")
            print(f"    Expression: {expression}")
            print(f"    Result: {result}")
            print("-" * 40)
        
        print(f"\nTotal records shown: {len(history)}")
        
    except Exception as e:
        print(f"Error retrieving history: {e}")

def clear_all_history():
    """Clear all calculation history with confirmation"""
    print("=" * 60)
    print("CLEAR CALCULATION HISTORY")
    print("=" * 60)
    
    try:
        # Get current count
        history = get_history(limit=1)
        if not history:
            print("No history to clear.")
            return
        
        print("WARNING: This will delete ALL calculation history!")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        
        if confirm.lower() == 'yes':
            success = clear_history()
            if success:
                print("✅ History cleared successfully!")
            else:
                print("❌ Failed to clear history")
        else:
            print("Operation cancelled.")
            
    except Exception as e:
        print(f"Error clearing history: {e}")

def show_statistics():
    """Show basic statistics about calculations"""
    print("=" * 60)
    print("CALCULATION STATISTICS")
    print("=" * 60)
    
    try:
        history = get_history(limit=1000)  # Get more records for stats
        
        if not history:
            print("No calculation history found.")
            return
        
        total_calculations = len(history)
        
        # Count operations
        operations = {'+': 0, '-': 0, '*': 0, '/': 0}
        for record in history:
            expression = record[1]
            for op in operations:
                operations[op] += expression.count(op)
        
        print(f"Total Calculations: {total_calculations}")
        print(f"Addition operations: {operations['+']}")
        print(f"Subtraction operations: {operations['-']}")
        print(f"Multiplication operations: {operations['*']}")
        print(f"Division operations: {operations['/']}")
        
        # Show date range
        if history:
            oldest = min(record[3] for record in history)
            newest = max(record[3] for record in history)
            print(f"Date range: {oldest.strftime('%Y-%m-%d')} to {newest.strftime('%Y-%m-%d')}")
        
    except Exception as e:
        print(f"Error retrieving statistics: {e}")

def main():
    """Main menu for history management"""
    while True:
        print("\n" + "=" * 60)
        print("CALCULATION HISTORY MANAGER")
        print("=" * 60)
        print("1. View History")
        print("2. Show Statistics")
        print("3. Clear All History")
        print("4. Exit")
        print("-" * 60)
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            limit = input("How many records to show? (default 20): ").strip()
            try:
                limit = int(limit) if limit else 20
                display_history(limit)
            except ValueError:
                print("Invalid number, showing default 20 records")
                display_history()
        
        elif choice == '2':
            show_statistics()
        
        elif choice == '3':
            clear_all_history()
        
        elif choice == '4':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
