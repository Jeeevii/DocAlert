"""
DocAlert API Usage Examples
This file demonstrates various ways to use the enhanced DocAlert API.
"""

import requests
import json
import time

# Configuration
API_BASE = "http://127.0.0.1:8000"
PHONE_NUMBER = "+15102586918"  # Replace with your phone number

class DocAlertClient:
    """Simple client for DocAlert API."""
    
    def __init__(self, base_url: str = API_BASE):
        self.base_url = base_url
    
    def health_check(self):
        """Check if the API is healthy and configured."""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def make_call(self, phone_number: str, message: str, **kwargs):
        """Make a voice call with optional voicemail and SMS fallback."""
        payload = {
            "to_number": phone_number,
            "message": message,
            **kwargs
        }
        response = requests.post(f"{self.base_url}/make-call", json=payload)
        return response.json()
    
    def send_sms(self, phone_number: str, message: str):
        """Send an SMS message."""
        payload = {
            "to_number": phone_number,
            "message": message
        }
        response = requests.post(f"{self.base_url}/send-sms", json=payload)
        return response.json()
    
    def send_notification(self, phone_number: str, message: str, method: str = "both", **kwargs):
        """Send unified notification via SMS, call, or both."""
        payload = {
            "to_number": phone_number,
            "message": message,
            "method": method,
            **kwargs
        }
        response = requests.post(f"{self.base_url}/send-notification", json=payload)
        return response.json()

# Initialize client
client = DocAlertClient()

def example_basic_call():
    """Example: Basic voice call."""
    print("=== Basic Voice Call ===")
    result = client.make_call(
        phone_number=PHONE_NUMBER,
        message="Hello! This is a basic test call from DocAlert."
    )
    print(json.dumps(result, indent=2))
    return result

def example_voicemail_call():
    """Example: Voice call optimized for voicemail."""
    print("=== Voicemail-Optimized Call ===")
    result = client.make_call(
        phone_number=PHONE_NUMBER,
        message="Important: Your appointment is tomorrow at 2 PM. Please call back to confirm.",
        enable_voicemail=True
    )
    print(json.dumps(result, indent=2))
    return result

def example_call_with_sms_fallback():
    """Example: Call with automatic SMS fallback."""
    print("=== Call with SMS Fallback ===")
    result = client.make_call(
        phone_number=PHONE_NUMBER,
        message="Urgent: Server maintenance starting in 30 minutes.",
        enable_voicemail=True,
        fallback_to_sms=True
    )
    print(json.dumps(result, indent=2))
    return result

def example_sms_only():
    """Example: SMS-only notification."""
    print("=== SMS Only ===")
    result = client.send_sms(
        phone_number=PHONE_NUMBER,
        message="📱 Reminder: Your package has been delivered and is waiting for pickup."
    )
    print(json.dumps(result, indent=2))
    return result

def example_unified_notification():
    """Example: Unified notification (both SMS and call)."""
    print("=== Unified Notification (SMS + Call) ===")
    result = client.send_notification(
        phone_number=PHONE_NUMBER,
        message="Critical Alert: System backup failed. Immediate attention required.",
        method="both",
        enable_voicemail=True
    )
    print(json.dumps(result, indent=2))
    return result

def example_sms_only_notification():
    """Example: Notification via SMS only."""
    print("=== SMS-Only Notification ===")
    result = client.send_notification(
        phone_number=PHONE_NUMBER,
        message="📊 Daily Report: All systems operational. 99.9% uptime achieved.",
        method="sms"
    )
    print(json.dumps(result, indent=2))
    return result

def example_call_only_notification():
    """Example: Notification via call only."""
    print("=== Call-Only Notification ===")
    result = client.send_notification(
        phone_number=PHONE_NUMBER,
        message="Security Alert: Unusual login detected from new location. Please verify.",
        method="call",
        enable_voicemail=True
    )
    print(json.dumps(result, indent=2))
    return result

def run_all_examples():
    """Run all examples with user confirmation."""
    print("DocAlert API Examples")
    print("=" * 50)
    
    # Health check first
    print("Checking API health...")
    health = client.health_check()
    print(json.dumps(health, indent=2))
    
    if not health.get('twilio_configured', False):
        print("⚠️  Twilio not properly configured. Examples may fail.")
        return
    
    examples = [
        ("Basic Call", example_basic_call),
        ("Voicemail Call", example_voicemail_call),
        ("Call with SMS Fallback", example_call_with_sms_fallback),
        ("SMS Only", example_sms_only),
        ("Unified Notification", example_unified_notification),
        ("SMS-Only Notification", example_sms_only_notification),
        ("Call-Only Notification", example_call_only_notification),
    ]
    
    for name, func in examples:
        print(f"\n{name}")
        print("-" * len(name))
        
        run = input(f"Run {name} example? (y/N): ").strip().lower()
        if run == 'y':
            try:
                func()
                print("✅ Example completed successfully")
            except Exception as e:
                print(f"❌ Example failed: {e}")
        else:
            print("⏭️  Skipped")
        
        # Small delay between examples
        time.sleep(1)

if __name__ == "__main__":
    print("Before running examples, make sure to:")
    print("1. Update PHONE_NUMBER variable with your actual phone number")
    print("2. Ensure the DocAlert server is running (python main.py)")
    print("3. Have valid Twilio credentials in .env file")
    print()
    
    phone = input(f"Enter phone number for testing (current: {PHONE_NUMBER}): ").strip()
    if phone:
        PHONE_NUMBER = phone
    
    run_all_examples()
