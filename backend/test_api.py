"""
DocAlert API Test Script - Simple Voice Calls with CORS and API Key Authentication
This script demonstrates basic voice call functionality, CORS support, and API key usage.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API base URL and authentication
BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("DOCALERT_API_KEY")

if not API_KEY:
    print("❌ Error: DOCALERT_API_KEY not found in .env file")
    print("Run 'python generate_api_key.py' to generate one")
    exit(1)

# Headers for API authentication
HEADERS = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

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

def make_simple_call(phone_number: str, message: str):
    """Test the simplified call endpoint (good for Cortex.ai integration)."""
    try:
        # Test form data (like Cortex.ai would send) with API key header
        response = requests.post(
            f"{BASE_URL}/call", 
            data={
                "phone_number": phone_number,
                "message": message
            },
            headers={"X-API-Key": API_KEY}
        )
        
        print(f"Simple Call Response (Status: {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
    except Exception as e:
        print(f"Simple call request failed: {e}")
        return False

def make_test_call(phone_number: str, message: str):
    """Make a test call using the JSON API."""
    try:
        payload = {
            "to_number": phone_number,
            "message": message
        }
        
        response = requests.post(f"{BASE_URL}/make-call", json=payload, headers=HEADERS)
        
        print(f"JSON Call Response (Status: {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
    except Exception as e:
        print(f"JSON call request failed: {e}")
        return False

def make_predefined_test_call():
    """Make a call using the test endpoint."""
    try:
        response = requests.post(f"{BASE_URL}/test-call", headers=HEADERS)
        
        print(f"Test Call Response (Status: {response.status_code}):")
        print(json.dumps(response.json(), indent=2))
        
        return response.status_code == 200
    except Exception as e:
        print(f"Test call failed: {e}")
        return False

if __name__ == "__main__":
    print("=== DocAlert Voice Call Test with CORS ===\n")
    
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
    
    # Test custom calls
    print("3. Testing custom calls...")
    phone_number = input("Enter phone number for custom call (e.g., +15551234567) or press Enter to skip: ").strip()
    
    if phone_number:
        message = input("Enter message to speak (or press Enter for default): ").strip()
        if not message:
            message = "Hello! This is a custom test call from your DocAlert system."
        
        print("\n--- Simple Call Test (Cortex.ai style) ---")
        if make_simple_call(phone_number, message):
            print("✅ Simple call initiated successfully")
        else:
            print("❌ Simple call failed")
        
        print("\n--- JSON Call Test ---")
        if make_test_call(phone_number, message):
            print("✅ JSON call initiated successfully")
        else:
            print("❌ JSON call failed")
    else:
        print("Skipping custom call tests")
    
    print("\n=== Test Complete ===")
    print(f"🌐 API Documentation: {BASE_URL}/docs")
    print(f"🏥 API Health: {BASE_URL}/health")
    print(f"📞 Feature: Simple voice calls with API key authentication")
    print(f"🔗 CORS: Enabled for external integrations")
    print(f"🔑 API Key: {API_KEY}")
    print(f"🤖 Cortex.ai: Use POST {BASE_URL}/call with X-API-Key header")
    print(f"📚 Integration Guide: See CORTEX_INTEGRATION.md")
    print(f"💡 Note: Advanced features (SMS, voicemail) are available but commented out")
    print(f"💡 They will be enabled once Twilio verification is complete")
