"""
Full-Stack Calculator Startup Script
===================================

This script starts both the Flask backend API and React frontend
for the complete calculator application with database integration.
"""

import subprocess
import sys
import time
import os
import threading
import webbrowser
from pathlib import Path

def start_flask_server():
    """Start the Flask backend server"""
    print("🚀 Starting Flask Backend Server...")
    try:
        # Start Flask app
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting Flask server: {e}")
    except KeyboardInterrupt:
        print("🛑 Flask server stopped")

def start_react_app():
    """Start the React frontend"""
    print("🚀 Starting React Frontend...")
    try:
        # Check if node_modules exists
        if not Path("node_modules").exists():
            print("📦 Installing npm dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Start React development server
        subprocess.run(["npm", "start"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting React app: {e}")
    except KeyboardInterrupt:
        print("🛑 React app stopped")

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    # Check Python dependencies
    try:
        import flask
        import flask_cors
        import psycopg2
        print("✅ Python dependencies OK")
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Run: pip install flask flask-cors psycopg2-binary")
        return False
    
    # Check Node.js
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} found")
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False
    
    # Check npm
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()} found")
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False
    
    return True

def main():
    """Main function to start the full-stack application"""
    print("=" * 60)
    print("🧮 FULL-STACK CALCULATOR APPLICATION")
    print("=" * 60)
    print("Starting both Flask backend and React frontend...")
    print()
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Missing dependencies. Please install them first.")
        return
    
    print("✅ All dependencies found!")
    print()
    
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    print("⏳ Waiting for Flask server to start...")
    time.sleep(3)
    
    # Open browser after a delay
    def open_browser():
        time.sleep(5)  # Wait for React to start
        print("🌐 Opening browser...")
        webbrowser.open("http://localhost:3000")
    
    browser_thread = threading.Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Start React app (this will block)
    try:
        start_react_app()
    except KeyboardInterrupt:
        print("\n🛑 Shutting down full-stack application...")
        print("✅ Application stopped")

if __name__ == "__main__":
    main()
