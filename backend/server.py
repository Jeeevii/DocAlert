from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Literal
import os
from dotenv import load_dotenv
from twilio_speech import TwilioSpeechService

# Advanced features available but commented out
# from twilio_sms import TwilioSMSService  
# from twilio_voicemail import TwilioVoicemailService

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DocAlert API",
    description="API for sending voice alerts using Twilio",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize Twilio service
try:
    twilio_service = TwilioSpeechService()
except Exception as e:
    print(f"Warning: Twilio service initialization failed: {e}")
    twilio_service = None

# Pydantic models for request/response
class CallRequest(BaseModel):
    to_number: str = Field(..., description="Phone number to call (e.g., '+15551234567')")
    message: str = Field(..., description="Message to speak during the call", max_length=1000)
    callback_url: Optional[str] = Field(None, description="Optional webhook URL for TwiML")

class CallResponse(BaseModel):
    success: bool
    call_sid: Optional[str] = None
    message: str

# Advanced models available but commented out for future use
"""
class SMSRequest(BaseModel):
    to_number: str = Field(..., description="Phone number to send SMS to (e.g., '+15551234567')")
    message: str = Field(..., description="SMS message content", max_length=1600)

class NotificationRequest(BaseModel):
    to_number: str = Field(..., description="Phone number to contact (e.g., '+15551234567')")
    message: str = Field(..., description="Message content", max_length=1600)
    method: Literal["sms", "call", "both"] = Field("both", description="Notification method")
    enable_voicemail: bool = Field(True, description="Enable voicemail-friendly TwiML for calls")

class SMSResponse(BaseModel):
    success: bool
    sms_sid: Optional[str] = None
    message: str

class NotificationResponse(BaseModel):
    success: bool
    call_sid: Optional[str] = None
    sms_sid: Optional[str] = None
    message: str
    actions_taken: Optional[list] = None
    errors: Optional[list] = None
"""

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "DocAlert API is running",
        "status": "healthy",
        "version": "1.0.0",
        "cors_enabled": True
    }

@app.get("/health")
async def health_check():
    """Detailed health check with service status."""
    return {
        "status": "healthy",
        "service": "DocAlert API",
        "version": "1.0.0",
        "twilio_configured": twilio_service is not None,
        "cors_enabled": True,
        "endpoints": {
            "voice_calls": "/make-call",
            "test_call": "/test-call",
            "webhook": "/twiml"
        },
        "environment_variables": {
            "TWILIO_ACCOUNT_SID": bool(os.environ.get("TWILIO_ACCOUNT_SID")),
            "TWILIO_AUTH_TOKEN": bool(os.environ.get("TWILIO_AUTH_TOKEN")),
            "TWILIO_FROM_NUMBER": bool(os.environ.get("TWILIO_FROM_NUMBER")),
            "PHONE_NUMBER": bool(os.environ.get("PHONE_NUMBER"))
        }
    }

@app.post("/make-call", response_model=CallResponse)
async def make_call(call_request: CallRequest):
    """
    Make a simple phone call with a custom message.
    
    Args:
        call_request: Request containing phone number and message
        
    Returns:
        CallResponse with success status and call SID
    """
    if not twilio_service:
        raise HTTPException(
            status_code=500, 
            detail="Twilio service is not properly configured. Check environment variables."
        )
    
    try:
        # Validate phone number format (basic check)
        if not call_request.to_number.startswith('+'):
            raise HTTPException(
                status_code=400,
                detail="Phone number must be in international format (e.g., +15551234567)"
            )
        
        # Make the call
        call_sid = twilio_service.make_call(
            to_number=call_request.to_number,
            message=call_request.message,
            callback_url=call_request.callback_url
        )
        
        return CallResponse(
            success=True,
            call_sid=call_sid,
            message="Call initiated successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to make call: {str(e)}"
        )

@app.post("/call")
async def simple_call(phone_number: str, message: str):
    """
    Simplified endpoint for external integrations like Cortex.ai.
    Accepts simple form parameters instead of JSON body.
    
    Args:
        phone_number: Phone number to call (e.g., "+15551234567") 
        message: Message to speak during the call
        
    Returns:
        Simple success response
    """
    try:
        # Use the main call function
        result = await make_call(CallRequest(
            to_number=phone_number,
            message=message
        ))
        
        return {
            "success": True,
            "call_sid": result.call_sid,
            "message": "Voice call initiated successfully",
            "phone_number": phone_number
        }
        
    except HTTPException as e:
        return {
            "success": False,
            "error": e.detail,
            "phone_number": phone_number
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "phone_number": phone_number
        }

# Advanced endpoints available but commented out pending SMS verification
"""
@app.post("/send-sms", response_model=SMSResponse)
async def send_sms(sms_request: SMSRequest):
    # SMS functionality available but commented out
    # Will be enabled once Twilio SMS verification is complete
    raise HTTPException(
        status_code=501,
        detail="SMS functionality temporarily disabled pending Twilio verification"
    )

@app.post("/send-notification", response_model=NotificationResponse)  
async def send_notification(notification_request: NotificationRequest):
    # Unified notification functionality available but commented out
    # Will be enabled once Twilio SMS verification is complete
    raise HTTPException(
        status_code=501,
        detail="Unified notifications temporarily disabled pending Twilio verification"
    )
"""

@app.post("/twiml")
async def twiml_webhook(message: str):
    """
    Webhook endpoint that returns TwiML for custom messages.
    This can be used as a callback URL for more complex call flows.
    """
    if not twilio_service:
        raise HTTPException(status_code=500, detail="Twilio service not configured")
    
    twiml_response = twilio_service.create_twiml_response(message)
    return Response(content=twiml_response, media_type="application/xml")

# Simple test endpoint for voice calls
@app.post("/test-call")
async def test_call():
    """Test endpoint that makes a simple call to a predefined number."""
    test_number = os.environ.get("PHONE_NUMBER")
    if not test_number:
        raise HTTPException(
            status_code=400,
            detail="PHONE_NUMBER environment variable not set"
        )
    
    return await make_call(CallRequest(
        to_number=test_number,
        message="This is a test call from your DocAlert system. If you can hear this message, the voice call system is working correctly."
    ))

# Advanced test endpoints available but commented out
"""
@app.post("/test-sms")
async def test_sms():
    # SMS test endpoint - will be enabled once verification is complete
    raise HTTPException(
        status_code=501,
        detail="SMS test temporarily disabled pending Twilio verification"
    )

@app.post("/test-notification")
async def test_notification():
    # Unified notification test - will be enabled once verification is complete
    raise HTTPException(
        status_code=501,
        detail="Notification test temporarily disabled pending Twilio verification"
    )
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)