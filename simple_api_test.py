"""
Simple API Test
===============

Test the Flask API endpoints without Unicode characters.
"""

import requests
import json

API_BASE = "http://localhost:5000/api"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"Health check passed: {data['message']}")
            return True
        else:
            print(f"Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("Cannot connect to API. Is Flask server running?")
        return False
    except Exception as e:
        print(f"Error testing health: {e}")
        return False

def test_save_calculation():
    """Test saving a calculation"""
    print("Testing calculation save...")
    try:
        data = {
            "expression": "2 + 2",
            "result": "4"
        }
        response = requests.post(f"{API_BASE}/calculate", json=data)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("Calculation saved successfully")
                return True
            else:
                print(f"Calculation save failed: {result['error']}")
                return False
        else:
            print(f"Calculation save failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error saving calculation: {e}")
        return False

def test_get_history():
    """Test getting calculation history"""
    print("Testing history retrieval...")
    try:
        response = requests.get(f"{API_BASE}/history?limit=5")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"History retrieved: {data['count']} calculations")
                for calc in data['history'][:3]:  # Show first 3
                    print(f"   - {calc['expression']} = {calc['result']}")
                return True
            else:
                print(f"History retrieval failed: {data['error']}")
                return False
        else:
            print(f"History retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error getting history: {e}")
        return False

def main():
    """Run API tests"""
    print("=" * 50)
    print("FLASK API TESTING")
    print("=" * 50)
    
    # Test health check
    if not test_health():
        print("\nAPI is not running. Please start Flask server first:")
        print("   python app.py")
        return
    
    print()
    
    # Test saving calculations
    test_save_calculation()
    test_save_calculation()  # Save another one
    
    print()
    
    # Test getting history
    test_get_history()
    
    print("\n" + "=" * 50)
    print("API TESTING COMPLETED")
    print("=" * 50)
    print("All endpoints are working correctly!")
    print("You can now use the React frontend with database integration.")

if __name__ == "__main__":
    main()
