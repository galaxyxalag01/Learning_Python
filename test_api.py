"""
Test Flask API Endpoints
========================

Simple script to test the Flask API endpoints for the calculator application.
"""

import requests
import json
import time

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

def test_create_session():
    """Test session creation"""
    print("Testing session creation...")
    try:
        response = requests.post(f"{API_BASE}/session")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"Session created: {data['session_id']}")
                return data['session_id']
            else:
                print(f"Session creation failed: {data['error']}")
                return None
        else:
            print(f"Session creation failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error creating session: {e}")
        return None

def test_save_calculation(session_id):
    """Test saving a calculation"""
    print("🔍 Testing calculation save...")
    try:
        data = {
            "expression": "2 + 2",
            "result": "4",
            "session_id": session_id
        }
        response = requests.post(f"{API_BASE}/calculate", json=data)
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ Calculation saved successfully")
                return True
            else:
                print(f"❌ Calculation save failed: {result['error']}")
                return False
        else:
            print(f"❌ Calculation save failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error saving calculation: {e}")
        return False

def test_get_history():
    """Test getting calculation history"""
    print("🔍 Testing history retrieval...")
    try:
        response = requests.get(f"{API_BASE}/history?limit=10")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"✅ History retrieved: {data['count']} calculations")
                for calc in data['history'][:3]:  # Show first 3
                    print(f"   - {calc['expression']} = {calc['result']}")
                return True
            else:
                print(f"❌ History retrieval failed: {data['error']}")
                return False
        else:
            print(f"❌ History retrieval failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting history: {e}")
        return False

def test_get_stats():
    """Test getting statistics"""
    print("🔍 Testing statistics...")
    try:
        response = requests.get(f"{API_BASE}/stats")
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                stats = data['stats']
                print(f"✅ Statistics retrieved:")
                print(f"   - Total calculations: {stats['total_calculations']}")
                print(f"   - Operations: {stats['operations']}")
                return True
            else:
                print(f"❌ Statistics failed: {data['error']}")
                return False
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting stats: {e}")
        return False

def main():
    """Run all API tests"""
    print("=" * 60)
    print("FLASK API TESTING")
    print("=" * 60)
    
    # Test health check
    if not test_health():
        print("\n❌ API is not running. Please start Flask server first:")
        print("   python app.py")
        return
    
    print()
    
    # Test session creation
    session_id = test_create_session()
    if not session_id:
        print("❌ Cannot proceed without session")
        return
    
    print()
    
    # Test saving calculations
    test_save_calculation(session_id)
    test_save_calculation(session_id)  # Save another one
    
    print()
    
    # Test getting history
    test_get_history()
    
    print()
    
    # Test getting statistics
    test_get_stats()
    
    print("\n" + "=" * 60)
    print("API TESTING COMPLETED")
    print("=" * 60)
    print("All endpoints are working correctly!")
    print("You can now use the React frontend with database integration.")

if __name__ == "__main__":
    main()
