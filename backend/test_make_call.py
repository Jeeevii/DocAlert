"""
Simple test for DocAlert /make-call endpoint
Focus on testing just the make-call endpoint with proper authentication
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:8000"
API_KEY = os.getenv("DOCALERT_API_KEY")

print(f"🔑 Using API Key: {API_KEY}")

def test_make_call_endpoint():
    """Test the /make-call endpoint specifically."""
    
    # Headers for X-API-Key authentication (matching server expectation)
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    # Test payload
    payload = {
        "to_number": "+15102586918",  # Your test number from .env
        "message": "This is a test call from DocAlert API testing"
    }
    
    print("🧪 Testing /make-call endpoint...")
    print(f"📞 Calling: {payload['to_number']}")
    print(f"💬 Message: {payload['message']}")
    print(f"🔗 URL: {BASE_URL}/make-call")
    print(f"🔑 Auth: X-API-Key {API_KEY[:8]}...")
    
    try:
        response = requests.post(
            f"{BASE_URL}/make-call",
            json=payload,
            headers=headers
        )
        
        print(f"\n📊 Response Status: {response.status_code}")
        print(f"📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(json.dumps(result, indent=2))
            return True
        else:
            print("❌ FAILED!")
            try:
                error_detail = response.json()
                print(json.dumps(error_detail, indent=2))
            except:
                print(f"Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {e}")
        return False

def test_health_check():
    """Test health check (no auth required)."""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        if response.status_code == 200:
            health_data = response.json()
            print(f"✅ Server is healthy!")
            print(f"📊 Twilio configured: {health_data.get('twilio_configured')}")
            return True
        return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    print("=== DocAlert /make-call Endpoint Test ===\n")
    
    if not API_KEY:
        print("❌ No API key found! Check your .env file.")
        exit(1)
    
    # Test health first
    print("1️⃣ Health Check...")
    if not test_health_check():
        print("💀 Server not responding! Start server first.")
        exit(1)
    
    print("\n2️⃣ Testing /make-call endpoint...")
    success = test_make_call_endpoint()
    
    if success:
        print("\n🎉 All tests passed! Your API is working correctly.")
    else:
        print("\n💥 Test failed. Check the error details above.")
