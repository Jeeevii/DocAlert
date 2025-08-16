"""
Twilio Voicemail Service
This module handles advanced voicemail functionality for DocAlert.
Currently disabled pending Twilio verification.
"""

import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from typing import Optional

class TwilioVoicemailService:
    """Voicemail service for Twilio - currently disabled."""
    
    def __init__(self):
        """Initialize Twilio client for voicemail."""
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER", "+18337647330")
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in environment variables")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def create_voicemail_twiml(self, message: str) -> str:
        """Create TwiML specifically for voicemail scenarios."""
        response = VoiceResponse()
        response.say("Hello, you have received an important notification.", voice='alice', language='en-US')
        response.pause(length=1)
        response.say(message, voice='alice', language='en-US')
        response.pause(length=2)
        response.say("I will repeat this message once more.", voice='alice')
        response.pause(length=1)
        response.say(message, voice='alice', language='en-US')
        response.say("This automated message was sent by DocAlert. Goodbye.", voice='alice')
        return str(response)
    
    def create_enhanced_twiml(self, message: str) -> str:
        """Create enhanced TwiML with voicemail support."""
        response = VoiceResponse()
        
        # Say the message
        response.say(message, voice='alice', language='en-US')
        
        # Add voicemail functionality
        response.say("If you missed this message, it will be repeated once more.", voice='alice')
        response.pause(length=2)
        response.say(message, voice='alice', language='en-US')
        response.say("This message was sent by DocAlert. Thank you.", voice='alice')
        
        return str(response)

# Example usage (when run directly)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    print("Voicemail Service - Currently disabled pending verification")
    print("This module will be enabled once Twilio verification is complete")
