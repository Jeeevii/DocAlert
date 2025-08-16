"""
DocAlert API Test Script - Simple Voice Calls
This script demonstrates basic voice call functionality.
"""

import requests
import json

# API base URL
BASE_URL = "http://127.0.0.1:8000"

def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print("Health Check Response:")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def make_test_call(phone_number: str, message: str):
    """Make a simple test call using the API."""
    try:
        payload = {
            "to_number": phone_number,
            "message": message
        }
        
        response = requests.post(f"{BASE_URL}/make-call", json=payload)
        
        print(f"Call Request Response (Status: {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
    except Exception as e:
        print(f"Call request failed: {e}")
        return False

def make_predefined_test_call():
    """Make a call using the test endpoint."""
    try:
        response = requests.post(f"{BASE_URL}/test-call")
        
        print(f"Test Call Response (Status: {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
    except Exception as e:
        print(f"Test call failed: {e}")
        return False

if __name__ == "__main__":
    print("=== DocAlert Voice Call Test ===\n")
    
    # Test health check
    print("1. Testing health check...")
    if test_health_check():
        print("✅ Health check passed\n")
    else:
        print("❌ Health check failed\n")
        exit(1)
    
    # Test predefined call
    print("2. Testing predefined test call...")
    if make_predefined_test_call():
        print("✅ Test call initiated successfully\n")
    else:
        print("❌ Test call failed\n")
    
    # Test custom call
    print("3. Testing custom call...")
    phone_number = input("Enter phone number for custom call (e.g., +15551234567) or press Enter to skip: ").strip()
    
    if phone_number:
        message = input("Enter message to speak (or press Enter for default): ").strip()
        if not message:
            message = "Hello! This is a custom test call from your DocAlert system."
        
        if make_test_call(phone_number, message):
            print("✅ Custom call initiated successfully")
        else:
            print("❌ Custom call failed")
    else:
        print("Skipping custom call test")
    
    print("\n=== Test Complete ===")
    print(f"🌐 API Documentation: {BASE_URL}/docs")
    print(f"🏥 API Health: {BASE_URL}/health")
    print(f"📞 Feature: Simple voice calls")
    print(f"� Note: Advanced features (SMS, voicemail) are available but commented out")
    print(f"� They will be enabled once Twilio verification is complete")
