"""
Enhanced Calculator Application with Database Integration
========================================================

A professional calculator with modern GUI, database storage,
and calculation history features.

Features:
- Basic arithmetic operations (+, -, ×, ÷)
- Database storage of calculations
- Calculation history viewing
- Session tracking
- Modern UI with theme switching
- Keyboard support

Author: Enhanced Calculator App
Version: 2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import re
import uuid
from datetime import datetime
from database_helper import CalculatorDB, save_calculation, get_history, clear_history

class EnhancedCalculatorApp:
    """
    Enhanced calculator application with database integration
    """
    
    def __init__(self, root):
        """Initialize the enhanced calculator application"""
        self.root = root
        self.root.title("Enhanced Calculator with Database")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Calculator state variables
        self.current_expression = ""
        self.result = ""
        self.memory = 0
        self.is_dark_theme = False
        self.session_id = str(uuid.uuid4())
        
        # Database connection
        self.db = CalculatorDB()
        self.db.create_session(self.session_id)
        
        # Initialize GUI components
        self.setup_styles()
        self.create_widgets()
        self.bind_keyboard_events()
        self.apply_theme()
        self.center_window()
    
    def setup_styles(self):
        """Configure visual styles for buttons and display"""
        self.style = ttk.Style()
        
        # Light theme colors
        self.light_colors = {
            'bg': '#f0f0f0',
            'display_bg': '#ffffff',
            'display_fg': '#000000',
            'button_bg': '#e0e0e0',
            'button_fg': '#000000',
            'button_hover': '#d0d0d0',
            'operator_bg': '#ff9500',
            'operator_fg': '#ffffff',
            'operator_hover': '#ff7f00',
            'function_bg': '#a6a6a6',
            'function_fg': '#000000',
            'function_hover': '#999999',
            'history_bg': '#f8f9fa',
            'history_fg': '#495057'
        }
        
        # Dark theme colors
        self.dark_colors = {
            'bg': '#1c1c1e',
            'display_bg': '#000000',
            'display_fg': '#ffffff',
            'button_bg': '#333333',
            'button_fg': '#ffffff',
            'button_hover': '#404040',
            'operator_bg': '#ff9500',
            'operator_fg': '#ffffff',
            'operator_hover': '#ff7f00',
            'function_bg': '#a6a6a6',
            'function_fg': '#000000',
            'function_hover': '#999999',
            'history_bg': '#2d2d30',
            'history_fg': '#cccccc'
        }
        
        self.current_colors = self.light_colors
    
    def apply_theme(self):
        """Apply the current theme colors to the application"""
        colors = self.current_colors
        self.root.configure(bg=colors['bg'])
        
        # Configure display colors
        self.display.configure(
            bg=colors['display_bg'],
            fg=colors['display_fg']
        )
        
        # Configure history display
        self.history_display.configure(
            bg=colors['history_bg'],
            fg=colors['history_fg']
        )
    
    def create_widgets(self):
        """Create and layout all GUI components"""
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.current_colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header with theme toggle and history button
        self.create_header(main_frame)
        
        # Display area
        self.create_display(main_frame)
        
        # History display
        self.create_history_display(main_frame)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.current_colors['bg'])
        button_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create buttons
        self.create_buttons(button_frame)
    
    def create_header(self, parent):
        """Create header with theme toggle and history button"""
        header_frame = tk.Frame(parent, bg=self.current_colors['bg'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="Enhanced Calculator",
            font=('Arial', 16, 'bold'),
            bg=self.current_colors['bg'],
            fg=self.current_colors['display_fg']
        )
        title_label.pack(side=tk.LEFT)
        
        # Theme toggle button
        self.theme_button = tk.Button(
            header_frame,
            text="🌙 Dark" if not self.is_dark_theme else "☀️ Light",
            command=self.toggle_theme,
            font=('Arial', 10),
            bg=self.current_colors['button_bg'],
            fg=self.current_colors['button_fg'],
            relief='raised',
            bd=1,
            padx=8,
            pady=4
        )
        self.theme_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # History button
        self.history_button = tk.Button(
            header_frame,
            text="📊 History",
            command=self.show_history,
            font=('Arial', 10),
            bg=self.current_colors['function_bg'],
            fg=self.current_colors['function_fg'],
            relief='raised',
            bd=1,
            padx=8,
            pady=4
        )
        self.history_button.pack(side=tk.RIGHT, padx=(5, 0))
    
    def create_display(self, parent):
        """Create the display area for showing expressions and results"""
        display_frame = tk.Frame(parent, bg=self.current_colors['bg'])
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Expression display (shows current input)
        self.expression_display = tk.Label(
            display_frame,
            text="",
            font=('Arial', 12),
            bg=self.current_colors['display_bg'],
            fg=self.current_colors['display_fg'],
            anchor='e',
            relief='sunken',
            bd=2,
            padx=10,
            pady=5
        )
        self.expression_display.pack(fill=tk.X, pady=(0, 5))
        
        # Result display (shows calculated result)
        self.display = tk.Label(
            display_frame,
            text="0",
            font=('Arial', 24, 'bold'),
            bg=self.current_colors['display_bg'],
            fg=self.current_colors['display_fg'],
            anchor='e',
            relief='sunken',
            bd=2,
            padx=10,
            pady=10
        )
        self.display.pack(fill=tk.X)
    
    def create_history_display(self, parent):
        """Create history display area"""
        history_frame = tk.Frame(parent, bg=self.current_colors['bg'])
        history_frame.pack(fill=tk.X, pady=(0, 10))
        
        # History label
        history_label = tk.Label(
            history_frame,
            text="Recent Calculations:",
            font=('Arial', 10, 'bold'),
            bg=self.current_colors['bg'],
            fg=self.current_colors['display_fg']
        )
        history_label.pack(anchor='w')
        
        # History display with scrollbar
        history_container = tk.Frame(history_frame, bg=self.current_colors['bg'])
        history_container.pack(fill=tk.X, pady=(5, 0))
        
        self.history_display = tk.Text(
            history_container,
            height=4,
            font=('Arial', 9),
            bg=self.current_colors['history_bg'],
            fg=self.current_colors['history_fg'],
            relief='sunken',
            bd=1,
            state='disabled',
            wrap='word'
        )
        
        scrollbar = tk.Scrollbar(history_container, orient='vertical', command=self.history_display.yview)
        self.history_display.configure(yscrollcommand=scrollbar.set)
        
        self.history_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Load and display recent history
        self.load_recent_history()
    
    def create_buttons(self, parent):
        """Create all calculator buttons with proper layout and styling"""
        # Button configuration
        button_config = {
            'font': ('Arial', 14, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'width': 5,
            'height': 2
        }
        
        # Button layout grid
        buttons = [
            # Row 1: Memory and Clear functions
            [('MC', self.memory_clear), ('MR', self.memory_recall), ('M+', self.memory_add), ('M-', self.memory_subtract)],
            # Row 2: Clear and operators
            [('AC', self.all_clear), ('C', self.clear), ('⌫', self.backspace), ('÷', lambda: self.add_operator('/'))],
            # Row 3: Numbers and operators
            [('7', lambda: self.add_number('7')), ('8', lambda: self.add_number('8')), ('9', lambda: self.add_number('9')), ('×', lambda: self.add_operator('*'))],
            # Row 4: Numbers and operators
            [('4', lambda: self.add_number('4')), ('5', lambda: self.add_number('5')), ('6', lambda: self.add_number('6')), ('-', lambda: self.add_operator('-'))],
            # Row 5: Numbers and operators
            [('1', lambda: self.add_number('1')), ('2', lambda: self.add_number('2')), ('3', lambda: self.add_number('3')), ('+', lambda: self.add_operator('+'))],
            # Row 6: Zero, decimal, and equals
            [('0', lambda: self.add_number('0')), ('.', self.add_decimal), ('=', self.calculate)]
        ]
        
        # Create buttons with proper styling
        for row_idx, row in enumerate(buttons):
            for col_idx, (text, command) in enumerate(row):
                button = tk.Button(
                    parent,
                    text=text,
                    command=command,
                    **button_config
                )
                
                # Apply button styling based on type
                self.style_button(button, text)
                
                # Add hover effects
                self.add_hover_effects(button, text)
                
                # Grid layout
                if text == '0':  # Zero button spans two columns
                    button.grid(row=row_idx, column=col_idx, columnspan=2, sticky='nsew', padx=2, pady=2)
                else:
                    button.grid(row=row_idx, column=col_idx, sticky='nsew', padx=2, pady=2)
        
        # Configure grid weights for proper resizing
        for i in range(4):
            parent.grid_columnconfigure(i, weight=1)
        for i in range(6):
            parent.grid_rowconfigure(i, weight=1)
    
    def style_button(self, button, text):
        """Apply appropriate styling to buttons based on their function"""
        colors = self.current_colors
        
        if text in ['MC', 'MR', 'M+', 'M-']:  # Memory buttons
            button.configure(
                bg=colors['function_bg'],
                fg=colors['function_fg'],
                activebackground=colors['function_hover']
            )
        elif text in ['AC', 'C', '⌫']:  # Clear buttons
            button.configure(
                bg=colors['function_bg'],
                fg=colors['function_fg'],
                activebackground=colors['function_hover']
            )
        elif text in ['+', '-', '×', '÷', '=']:  # Operator buttons
            button.configure(
                bg=colors['operator_bg'],
                fg=colors['operator_fg'],
                activebackground=colors['operator_hover']
            )
        else:  # Number buttons
            button.configure(
                bg=colors['button_bg'],
                fg=colors['button_fg'],
                activebackground=colors['button_hover']
            )
    
    def add_hover_effects(self, button, text):
        """Add hover effects to buttons for better user interaction"""
        colors = self.current_colors
        
        def on_enter(event):
            if text in ['MC', 'MR', 'M+', 'M-', 'AC', 'C', '⌫']:
                button.configure(bg=colors['function_hover'])
            elif text in ['+', '-', '×', '÷', '=']:
                button.configure(bg=colors['operator_hover'])
            else:
                button.configure(bg=colors['button_hover'])
        
        def on_leave(event):
            self.style_button(button, text)
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
    
    def toggle_theme(self):
        """Toggle between light and dark themes"""
        self.is_dark_theme = not self.is_dark_theme
        self.current_colors = self.dark_colors if self.is_dark_theme else self.light_colors
        
        # Update theme button text
        self.theme_button.configure(
            text="☀️ Light" if self.is_dark_theme else "🌙 Dark"
        )
        
        # Reapply theme to all components
        self.apply_theme()
        self.update_all_button_styles()
        self.load_recent_history()
    
    def update_all_button_styles(self):
        """Update styling for all buttons when theme changes"""
        for widget in self.root.winfo_children():
            self.update_widget_styles(widget)
    
    def update_widget_styles(self, widget):
        """Recursively update widget styles for theme changes"""
        if isinstance(widget, tk.Button):
            # Find button text to determine proper styling
            text = widget.cget('text')
            self.style_button(widget, text)
            self.add_hover_effects(widget, text)
        
        # Recursively update child widgets
        for child in widget.winfo_children():
            self.update_widget_styles(child)
    
    def bind_keyboard_events(self):
        """Bind keyboard events for calculator input"""
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def on_key_press(self, event):
        """Handle keyboard input events"""
        key = event.char
        
        # Number keys
        if key.isdigit():
            self.add_number(key)
        # Decimal point
        elif key == '.':
            self.add_decimal()
        # Operators
        elif key in ['+', '-', '*', '/']:
            self.add_operator(key)
        # Equals
        elif key in ['=', '\r']:  # Enter key
            self.calculate()
        # Clear
        elif key.lower() == 'c':
            self.clear()
        # All Clear
        elif key.lower() == 'a':
            self.all_clear()
        # Backspace
        elif event.keysym == 'BackSpace':
            self.backspace()
        # Escape
        elif event.keysym == 'Escape':
            self.all_clear()
    
    def add_number(self, number):
        """Add a number to the current expression"""
        if self.result and not self.current_expression:
            self.current_expression = ""
        
        self.current_expression += number
        self.update_display()
    
    def add_operator(self, operator):
        """Add an operator to the current expression"""
        if not self.current_expression:
            if self.result:
                self.current_expression = str(self.result)
            else:
                return
        
        # Replace last operator if it exists
        if self.current_expression and self.current_expression[-1] in ['+', '-', '*', '/']:
            self.current_expression = self.current_expression[:-1]
        
        self.current_expression += operator
        self.update_display()
    
    def add_decimal(self):
        """Add a decimal point to the current number"""
        if not self.current_expression:
            self.current_expression = "0."
        elif self.current_expression[-1] not in ['.', '+', '-', '*', '/']:
            # Check if current number already has decimal
            last_number = re.split(r'[+\-*/]', self.current_expression)[-1]
            if '.' not in last_number:
                self.current_expression += '.'
        
        self.update_display()
    
    def clear(self):
        """Clear the last entry (C button)"""
        if self.current_expression:
            self.current_expression = ""
            self.update_display()
    
    def all_clear(self):
        """Clear everything (AC button)"""
        self.current_expression = ""
        self.result = ""
        self.update_display()
    
    def backspace(self):
        """Remove the last character from the expression"""
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self.update_display()
    
    def calculate(self):
        """Calculate the result of the current expression and save to database"""
        if not self.current_expression:
            return
        
        try:
            # Replace display symbols with Python operators
            expression = self.current_expression.replace('×', '*').replace('÷', '/')
            
            # Evaluate the expression safely
            result = eval(expression)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)  # Limit decimal places
            
            self.result = result
            self.current_expression = ""
            self.update_display()
            
            # Save to database
            self.save_calculation_to_db(expression, str(result))
            
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
        except Exception as e:
            self.show_error("Invalid expression")
    
    def save_calculation_to_db(self, expression, result):
        """Save calculation to database and update history display"""
        try:
            # Save to database
            success = save_calculation(expression, result, self.session_id)
            if success:
                # Update history display
                self.load_recent_history()
        except Exception as e:
            print(f"Error saving to database: {e}")
    
    def load_recent_history(self):
        """Load and display recent calculation history"""
        try:
            history = get_history(limit=5)
            
            # Clear current history display
            self.history_display.configure(state='normal')
            self.history_display.delete(1.0, tk.END)
            
            if history:
                for record in history:
                    expression, result, timestamp = record[1], record[2], record[3]
                    time_str = timestamp.strftime("%H:%M")
                    history_text = f"{time_str}: {expression} = {result}\n"
                    self.history_display.insert(tk.END, history_text)
            else:
                self.history_display.insert(tk.END, "No calculations yet")
            
            self.history_display.configure(state='disabled')
            
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def show_history(self):
        """Show detailed calculation history in a new window"""
        try:
            history = get_history(limit=50)
            
            # Create history window
            history_window = tk.Toplevel(self.root)
            history_window.title("Calculation History")
            history_window.geometry("500x400")
            history_window.configure(bg=self.current_colors['bg'])
            
            # History text widget with scrollbar
            history_frame = tk.Frame(history_window, bg=self.current_colors['bg'])
            history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            history_text = tk.Text(
                history_frame,
                font=('Arial', 10),
                bg=self.current_colors['history_bg'],
                fg=self.current_colors['history_fg'],
                wrap='word'
            )
            
            scrollbar = tk.Scrollbar(history_frame, orient='vertical', command=history_text.yview)
            history_text.configure(yscrollcommand=scrollbar.set)
            
            history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Add history data
            if history:
                for record in history:
                    expression, result, timestamp = record[1], record[2], record[3]
                    time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    history_text.insert(tk.END, f"{time_str}\n")
                    history_text.insert(tk.END, f"  {expression} = {result}\n\n")
            else:
                history_text.insert(tk.END, "No calculation history found")
            
            history_text.configure(state='disabled')
            
            # Clear history button
            clear_button = tk.Button(
                history_window,
                text="Clear All History",
                command=lambda: self.clear_all_history(history_window),
                bg=self.current_colors['function_bg'],
                fg=self.current_colors['function_fg'],
                font=('Arial', 10, 'bold')
            )
            clear_button.pack(pady=10)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error loading history: {e}")
    
    def clear_all_history(self, window):
        """Clear all calculation history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all history?"):
            try:
                success = clear_history()
                if success:
                    messagebox.showinfo("Success", "History cleared successfully!")
                    window.destroy()
                    self.load_recent_history()
                else:
                    messagebox.showerror("Error", "Failed to clear history")
            except Exception as e:
                messagebox.showerror("Error", f"Error clearing history: {e}")
    
    def show_error(self, message):
        """Display error message to user"""
        self.display.configure(text="Error")
        self.expression_display.configure(text=message)
        self.current_expression = ""
        self.result = ""
    
    def update_display(self):
        """Update the display with current expression and result"""
        # Update expression display
        self.expression_display.configure(text=self.current_expression or "")
        
        # Update result display
        if self.result != "":
            self.display.configure(text=str(self.result))
        else:
            self.display.configure(text="0")
    
    def memory_clear(self):
        """Clear memory (MC button)"""
        self.memory = 0
    
    def memory_recall(self):
        """Recall value from memory (MR button)"""
        if self.memory != 0:
            self.current_expression = str(self.memory)
            self.update_display()
    
    def memory_add(self):
        """Add current result to memory (M+ button)"""
        try:
            if self.result:
                self.memory += float(self.result)
            elif self.current_expression:
                self.memory += float(eval(self.current_expression))
        except:
            pass
    
    def memory_subtract(self):
        """Subtract current result from memory (M- button)"""
        try:
            if self.result:
                self.memory -= float(self.result)
            elif self.current_expression:
                self.memory -= float(eval(self.current_expression))
        except:
            pass
    
    def center_window(self):
        """Center the calculator window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def __del__(self):
        """Cleanup when application closes"""
        if hasattr(self, 'db'):
            self.db.disconnect()


def main():
    """Main function to run the enhanced calculator application"""
    # Create the main window
    root = tk.Tk()
    
    # Create and run the enhanced calculator application
    app = EnhancedCalculatorApp(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
