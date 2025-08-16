"""
Twilio SMS Service
This module handles SMS functionality for DocAlert.
Currently disabled pending Twilio SMS verification.
"""

import os
from twilio.rest import Client
from typing import Optional, Dict, Any

class TwilioSMSService:
    """SMS service for Twilio - currently disabled."""
    
    def __init__(self):
        """Initialize Twilio client for SMS."""
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER", "+18337647330")
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in environment variables")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def send_sms(self, to_number: str, message: str) -> str:
        """
        Send an SMS message.
        
        Args:
            to_number: Phone number to send SMS to (e.g., "+15551234567")
            message: Message content (max 1600 characters)
            
        Returns:
            Message SID
        """
        try:
            # Ensure message isn't too long for SMS
            if len(message) > 1600:
                message = message[:1597] + "..."
            
            sms = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            return sms.sid
            
        except Exception as e:
            raise Exception(f"Failed to send SMS: {str(e)}")

# Example usage (when run directly)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("SMS Service - Currently disabled pending verification")
    print("This module will be enabled once Twilio SMS is verified")
