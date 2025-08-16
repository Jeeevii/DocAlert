from fastapi import FastAPI, HTTPException, Depends, Header, File, UploadFile, Form
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import Optional, Literal, Annotated, List
import os
from dotenv import load_dotenv
from twilio_speech import TwilioSpeechService

# Advanced features available but commented out
# from twilio_sms import TwilioSMSService  
# from twilio_voicemail import TwilioVoicemailService

# Document parsing service
try:
    from enhanced_document_parser import EnhancedDocumentParser
    document_parser = EnhancedDocumentParser()
    print("✅ Enhanced document parser initialized successfully")
except ImportError as e:
    print(f"❌ Enhanced document parser not available: {e}")
    document_parser = None

# Load environment variables
load_dotenv()

# API Key configuration
API_KEY = os.getenv("DOCALERT_API_KEY")
if not API_KEY:
    raise ValueError("DOCALERT_API_KEY environment variable is required")

# Security scheme
security = HTTPBearer()

def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verify the API key from the Authorization header."""
    if credentials.credentials != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

def verify_api_key_header(x_api_key: Annotated[str | None, Header()] = None) -> str:
    """Alternative API key verification via X-API-Key header."""
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key. Please provide a valid API key in X-API-Key header.",
        )
    return x_api_key

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

# Document parsing models
class DocumentParseRequest(BaseModel):
    template_type: Optional[str] = Field(None, description="Document template type (employment_form, tax_form, address_verification)")
    auto_detect: bool = Field(True, description="Auto-detect document fields if no template specified")

class DocumentField(BaseModel):
    page: int
    title: str
    question: str
    answer: str
    optional: bool
    required: bool
    field_type: str
    format_expectation: str
    confidence: float = 0.0
    validation_status: str = "PENDING"
    validation_errors: List[str] = []

class ValidationSummary(BaseModel):
    total_fields: int
    passed: int
    failed: int
    warnings: int
    missing_required: int
    validation_percentage: float
    ready_for_processing: bool

class DocumentParseResponse(BaseModel):
    success: bool
    filename: Optional[str] = None
    template_type: Optional[str] = None
    page_count: Optional[int] = None
    fields: List[DocumentField] = []
    validation_summary: Optional[ValidationSummary] = None
    raw_text: Optional[str] = None
    error: Optional[str] = None

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
        "document_parsing_configured": document_parser is not None,
        "cors_enabled": True,
        "endpoints": {
            "voice_calls": "/make-call",
            "test_call": "/test-call",
            "webhook": "/twiml",
            "document_parsing": "/parse-document",
            "document_templates": "/document-templates",
            "field_validation": "/validate-document-field",
            "test_llm_parsing": "/test-llm-parsing"
        },
        "environment_variables": {
            "TWILIO_ACCOUNT_SID": bool(os.environ.get("TWILIO_ACCOUNT_SID")),
            "TWILIO_AUTH_TOKEN": bool(os.environ.get("TWILIO_AUTH_TOKEN")),
            "TWILIO_FROM_NUMBER": bool(os.environ.get("TWILIO_FROM_NUMBER")),
            "PHONE_NUMBER": bool(os.environ.get("PHONE_NUMBER"))
        }
    }

@app.post("/make-call", response_model=CallResponse)
async def make_call(call_request: CallRequest, api_key: str = Depends(verify_api_key_header)):
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

# Document parsing endpoints
@app.post("/parse-document")
async def parse_document(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key_header)
):
    """
    Parse a document with comprehensive structure analysis optimized for LLM processing.
    
    This endpoint provides:
    - Page-by-page content breakdown
    - Content block classification
    - Pattern detection for forms, fields, signatures
    - Text confidence scoring
    - Processing instructions for LLMs
    
    Args:
        file: The document file to parse (PDF or image)
        
    Returns:
        Comprehensive document structure with LLM processing guidance
    """
    if not document_parser:
        raise HTTPException(
            status_code=501,
            detail="Document parsing not available. Install pypdf to enable this feature."
        )
    
    # Validate file type
    allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.bmp'}
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file_extension}. Supported: {', '.join(allowed_extensions)}"
        )
    
    try:
        # Read file content
        file_content = await file.read()
        
        if len(file_content) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Parse document with enhanced parser for LLM
        result = await document_parser.parse_document_for_llm(
            file_content=file_content,
            filename=file.filename
        )
        
        if not result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Document parsing failed: {result.get('error', 'Unknown error')}"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )

@app.get("/document-templates")
async def get_document_templates(api_key: str = Depends(verify_api_key_header)):
    """
    Get available document templates for parsing.
    
    Returns:
        List of available templates and their field definitions
    """
    if not document_parser:
        raise HTTPException(
            status_code=501,
            detail="Document parsing not available. Install pypdf to enable this feature."
        )
    
    # Return template info for enhanced parser
    return {
        "success": True,
        "templates": {
            "enhanced": "LLM-optimized parsing with comprehensive structure analysis"
        },
        "supported_field_types": ["name", "address", "phone", "email", "date", "ssn"],
        "supported_file_types": [".pdf", ".png", ".jpg", ".jpeg", ".tiff", ".bmp"],
        "parsing_modes": {
            "enhanced_llm": "Comprehensive document analysis for LLM processing"
        }
    }

@app.post("/validate-document-field")
async def validate_document_field(
    field_type: str = Form(...),
    field_value: str = Form(...),
    api_key: str = Depends(verify_api_key_header)
):
    """
    Validate a single field value against its expected format.
    
    Args:
        field_type: The type of field (ssn, date, email, phone, etc.)
        field_value: The value to validate
        
    Returns:
        Validation result
    """
    if not document_parser:
        raise HTTPException(
            status_code=501,
            detail="Document parsing not available. Install pypdf to enable this feature."
        )
    
    try:
        # Simple validation patterns
        patterns = {
            "ssn": r'^\d{3}-?\d{2}-?\d{4}$',
            "date": r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$',
            "email": r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
            "phone": r'^\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$',
            "zip": r'^\d{5}(-\d{4})?$',
            "name": r'^[a-zA-Z\s\'-]{2,}$'
        }
        
        field_type_lower = field_type.lower()
        pattern = patterns.get(field_type_lower, ".*")
        
        # Validate
        import re
        is_valid = re.match(pattern, field_value.strip()) is not None
        
        return {
            "success": True,
            "field_type": field_type,
            "field_value": field_value,
            "is_valid": is_valid,
            "pattern": pattern,
            "validation_message": "Valid format" if is_valid else f"Invalid format for {field_type}"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Validation error: {str(e)}"
        )

# Test endpoint for LLM parsing
@app.post("/test-llm-parsing")
async def test_llm_parsing(api_key: str = Depends(verify_api_key_header)):
    """
    Test the enhanced LLM document parsing with a sample document.
    This endpoint will attempt to parse your sample PDF for testing.
    """
    if not document_parser:
        raise HTTPException(
            status_code=501,
            detail="Enhanced document parsing not available."
        )
    
    # Check if the test document exists
    test_doc_path = "testing_doc/invalid_fw4.pdf"
    if not os.path.exists(test_doc_path):
        raise HTTPException(
            status_code=404,
            detail=f"Test document not found: {test_doc_path}. Please ensure the file exists in the backend directory."
        )
    
    try:
        # Read the test document
        with open(test_doc_path, 'rb') as f:
            file_content = f.read()
        
        # Parse with enhanced parser
        result = await document_parser.parse_document_for_llm(
            file_content=file_content,
            filename=test_doc_path
        )
        
        return {
            "test_status": "success",
            "message": "Enhanced LLM parsing test completed",
            "parsing_result": result
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Test parsing failed: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)