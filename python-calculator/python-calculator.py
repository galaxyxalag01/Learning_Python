"""
Modern Calculator Application using Python Tkinter
=================================================

A professional calculator with modern GUI, keyboard support, memory functions,
and theme switching capabilities.

Features:
- Basic arithmetic operations (+, -, ×, ÷)
- Decimal number support
- Clear (C) and All Clear (AC) functions
- Error handling for invalid inputs
- Keyboard input support
- Memory functions (M+, M-, MR, MC)
- Light/Dark theme toggle
- Modern UI with hover effects

Author: Python Calculator App
Version: 1.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import re


class CalculatorApp:
    """
    Main calculator application class that handles GUI creation,
    user input processing, and mathematical operations.
    """
    
    def __init__(self, root):
        """
        Initialize the calculator application.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Modern Calculator")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        self.root.configure(bg='#f0f0f0')
        
        # Calculator state variables
        self.current_expression = ""
        self.result = ""
        self.memory = 0
        self.is_dark_theme = False
        
        # Initialize GUI components
        self.setup_styles()
        self.create_widgets()
        self.bind_keyboard_events()
        
        # Apply theme after widgets are created
        self.apply_theme()
        
        # Center the window on screen
        self.center_window()
    
    def setup_styles(self):
        """
        Configure the visual styles for buttons and display.
        Creates both light and dark theme configurations.
        """
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
            'function_hover': '#999999'
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
            'function_hover': '#999999'
        }
        
        self.current_colors = self.light_colors
    
    def apply_theme(self):
        """
        Apply the current theme colors to the application.
        """
        colors = self.current_colors
        self.root.configure(bg=colors['bg'])
        
        # Configure display colors
        self.display.configure(
            bg=colors['display_bg'],
            fg=colors['display_fg']
        )
    
    def create_widgets(self):
        """
        Create and layout all GUI components including display,
        buttons, and control elements.
        """
        # Main frame
        main_frame = tk.Frame(self.root, bg=self.current_colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Display area
        self.create_display(main_frame)
        
        # Button frame
        button_frame = tk.Frame(main_frame, bg=self.current_colors['bg'])
        button_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Create buttons
        self.create_buttons(button_frame)
        
        # Theme toggle button
        self.create_theme_toggle(main_frame)
    
    def create_display(self, parent):
        """
        Create the display area for showing expressions and results.
        
        Args:
            parent: Parent widget for the display
        """
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
    
    def create_buttons(self, parent):
        """
        Create all calculator buttons with proper layout and styling.
        
        Args:
            parent: Parent widget for buttons
        """
        # Button configuration
        button_config = {
            'font': ('Arial', 16, 'bold'),
            'relief': 'raised',
            'bd': 2,
            'width': 6,
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
        """
        Apply appropriate styling to buttons based on their function.
        
        Args:
            button: Button widget to style
            text: Button text to determine styling
        """
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
        """
        Add hover effects to buttons for better user interaction.
        
        Args:
            button: Button widget
            text: Button text
        """
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
    
    def create_theme_toggle(self, parent):
        """
        Create theme toggle button for switching between light and dark themes.
        
        Args:
            parent: Parent widget for the toggle button
        """
        self.theme_button = tk.Button(
            parent,
            text="🌙 Dark" if not self.is_dark_theme else "☀️ Light",
            command=self.toggle_theme,
            font=('Arial', 12),
            bg=self.current_colors['button_bg'],
            fg=self.current_colors['button_fg'],
            relief='raised',
            bd=2,
            padx=10,
            pady=5
        )
        self.theme_button.pack(pady=(10, 0))
    
    def toggle_theme(self):
        """
        Toggle between light and dark themes.
        """
        self.is_dark_theme = not self.is_dark_theme
        self.current_colors = self.dark_colors if self.is_dark_theme else self.light_colors
        
        # Update theme button text
        self.theme_button.configure(
            text="☀️ Light" if self.is_dark_theme else "🌙 Dark"
        )
        
        # Reapply theme to all components
        self.apply_theme()
        self.update_all_button_styles()
    
    def update_all_button_styles(self):
        """
        Update styling for all buttons when theme changes.
        """
        for widget in self.root.winfo_children():
            self.update_widget_styles(widget)
    
    def update_widget_styles(self, widget):
        """
        Recursively update widget styles for theme changes.
        
        Args:
            widget: Widget to update
        """
        if isinstance(widget, tk.Button):
            # Find button text to determine proper styling
            text = widget.cget('text')
            self.style_button(widget, text)
            self.add_hover_effects(widget, text)
        
        # Recursively update child widgets
        for child in widget.winfo_children():
            self.update_widget_styles(child)
    
    def bind_keyboard_events(self):
        """
        Bind keyboard events for calculator input.
        """
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()
    
    def on_key_press(self, event):
        """
        Handle keyboard input events.
        
        Args:
            event: Keyboard event
        """
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
        """
        Add a number to the current expression.
        
        Args:
            number: Number to add (string)
        """
        if self.result and not self.current_expression:
            self.current_expression = ""
        
        self.current_expression += number
        self.update_display()
    
    def add_operator(self, operator):
        """
        Add an operator to the current expression.
        
        Args:
            operator: Operator to add (string)
        """
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
        """
        Add a decimal point to the current number.
        """
        if not self.current_expression:
            self.current_expression = "0."
        elif self.current_expression[-1] not in ['.', '+', '-', '*', '/']:
            # Check if current number already has decimal
            last_number = re.split(r'[+\-*/]', self.current_expression)[-1]
            if '.' not in last_number:
                self.current_expression += '.'
        
        self.update_display()
    
    def clear(self):
        """
        Clear the last entry (C button).
        """
        if self.current_expression:
            self.current_expression = ""
            self.update_display()
    
    def all_clear(self):
        """
        Clear everything (AC button).
        """
        self.current_expression = ""
        self.result = ""
        self.update_display()
    
    def backspace(self):
        """
        Remove the last character from the expression.
        """
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
            self.update_display()
    
    def calculate(self):
        """
        Calculate the result of the current expression.
        """
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
            
        except ZeroDivisionError:
            self.show_error("Cannot divide by zero")
        except Exception as e:
            self.show_error("Invalid expression")
    
    def show_error(self, message):
        """
        Display error message to user.
        
        Args:
            message: Error message to display
        """
        self.display.configure(text="Error")
        self.expression_display.configure(text=message)
        self.current_expression = ""
        self.result = ""
    
    def update_display(self):
        """
        Update the display with current expression and result.
        """
        # Update expression display
        self.expression_display.configure(text=self.current_expression or "")
        
        # Update result display
        if self.result != "":
            self.display.configure(text=str(self.result))
        else:
            self.display.configure(text="0")
    
    def memory_clear(self):
        """
        Clear memory (MC button).
        """
        self.memory = 0
    
    def memory_recall(self):
        """
        Recall value from memory (MR button).
        """
        if self.memory != 0:
            self.current_expression = str(self.memory)
            self.update_display()
    
    def memory_add(self):
        """
        Add current result to memory (M+ button).
        """
        try:
            if self.result:
                self.memory += float(self.result)
            elif self.current_expression:
                self.memory += float(eval(self.current_expression))
        except:
            pass
    
    def memory_subtract(self):
        """
        Subtract current result from memory (M- button).
        """
        try:
            if self.result:
                self.memory -= float(self.result)
            elif self.current_expression:
                self.memory -= float(eval(self.current_expression))
        except:
            pass
    
    def center_window(self):
        """
        Center the calculator window on the screen.
        """
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')


def main():
    """
    Main function to run the calculator application.
    """
    # Create the main window
    root = tk.Tk()
    
    # Create and run the calculator application
    app = CalculatorApp(root)
    
    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
