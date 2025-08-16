"""
Twilio Speech Service
Simple voice call functionality for DocAlert.
"""

import os
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from typing import Optional

class TwilioSpeechService:
    def __init__(self):
        """Initialize Twilio client with credentials from environment variables."""
        self.account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
        self.auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
        self.from_number = os.environ.get("TWILIO_FROM_NUMBER", "+18337647330")
        
        if not self.account_sid or not self.auth_token:
            raise ValueError("TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN must be set in environment variables")
        
        self.client = Client(self.account_sid, self.auth_token)
    
    def create_twiml_response(self, message: str) -> str:
        """Create simple TwiML response for text-to-speech."""
        response = VoiceResponse()
        response.say(message, voice='alice', language='en-US')
        return str(response)
    
    def make_call(self, to_number: str, message: str, callback_url: Optional[str] = None) -> str:
        """
        Make a simple phone call with a custom message.
        
        Args:
            to_number: Phone number to call (e.g., "+15551234567")
            message: Message to speak during the call
            callback_url: URL that serves TwiML for the call
            
        Returns:
            Call SID
        """
        try:
            # Create TwiML for the call
            if callback_url:
                # Use provided callback URL
                call = self.client.calls.create(
                    url=callback_url,
                    to=to_number,
                    from_=self.from_number
                )
            else:
                # Use inline TwiML
                twiml = self.create_twiml_response(message)
                call = self.client.calls.create(
                    twiml=twiml,
                    to=to_number,
                    from_=self.from_number
                )
            
            return call.sid
            
        except Exception as e:
            raise Exception(f"Failed to make call: {str(e)}")

# Backward compatibility
TwilioService = TwilioSpeechService

# Example usage (when run directly)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    service = TwilioSpeechService()
    
    # Example call
    test_number = os.environ.get("PHONE_NUMBER", "+15102586918")
    call_sid = service.make_call(
        to_number=test_number,
        message="Hello! This is a simple test call from your DocAlert system."
    )
    
    print(f"Call initiated with SID: {call_sid}")

# Example usage (when run directly)
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    service = TwilioSpeechService()
    
    # Example call
    call_sid = service.make_call(
        to_number="+15102586918",  # Replace with actual number
        message="Hello! This is a test message from your DocAlert system."
    )
    
    print(f"Call initiated with SID: {call_sid}")