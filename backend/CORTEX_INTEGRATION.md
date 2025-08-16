# DocAlert + Cortex.ai Integration Guide

This guide shows how to integrate DocAlert with Cortex.ai using HTTP requests.

## Server Setup

The DocAlert server now includes CORS support and simplified endpoints for external integrations.

### CORS Configuration
- ✅ **Allow Origins**: `*` (all origins)
- ✅ **Allow Methods**: `*` (all HTTP methods)
- ✅ **Allow Headers**: `*` (all headers)
- ✅ **Allow Credentials**: `true`

## Available Endpoints for Cortex.ai

### 1. Health Check
```
GET http://127.0.0.1:8000/health
```
**Response:**
```json
{
  "status": "healthy",
  "service": "DocAlert API",
  "version": "1.0.0",
  "twilio_configured": true,
  "cors_enabled": true,
  "endpoints": {
    "voice_calls": "/make-call",
    "test_call": "/test-call", 
    "webhook": "/twiml"
  }
}
```

### 2. Simple Call Endpoint (Recommended for Cortex.ai)
```
POST http://127.0.0.1:8000/call
Content-Type: application/x-www-form-urlencoded

phone_number=+15551234567&message=Hello from Cortex.ai!
```

**Response:**
```json
{
  "success": true,
  "call_sid": "CAxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "message": "Voice call initiated successfully",
  "phone_number": "+15551234567"
}
```

### 3. JSON Call Endpoint (Alternative)
```
POST http://127.0.0.1:8000/make-call
Content-Type: application/json

{
  "to_number": "+15551234567",
  "message": "Hello from Cortex.ai!"
}
```

## Cortex.ai Configuration

When setting up the HTTP action in Cortex.ai:

### Method 1: Simple Form Data (Recommended)
- **URL**: `http://127.0.0.1:8000/call`
- **Method**: `POST`
- **Content-Type**: `application/x-www-form-urlencoded`
- **Body**:
  ```
  phone_number={{phone_number}}
  message={{message}}
  ```

### Method 2: JSON Body
- **URL**: `http://127.0.0.1:8000/make-call`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "to_number": "{{phone_number}}",
    "message": "{{message}}"
  }
  ```

## Example Cortex.ai Use Cases

### 1. Emergency Alert
```
Action: HTTP Request
URL: http://127.0.0.1:8000/call
Method: POST
Body: phone_number=+15551234567&message=Emergency detected! Please check the system immediately.
```

### 2. Appointment Reminder
```
Action: HTTP Request  
URL: http://127.0.0.1:8000/call
Method: POST
Body: phone_number={{user.phone}}&message=Reminder: You have an appointment at {{appointment.time}}
```

### 3. System Alert
```
Action: HTTP Request
URL: http://127.0.0.1:8000/call
Method: POST
Body: phone_number={{admin.phone}}&message=System alert: {{alert.description}}. Immediate attention required.
```

## Error Handling

Both endpoints return consistent error responses:

**Success Response:**
```json
{
  "success": true,
  "call_sid": "CAxxxxx...",
  "message": "Voice call initiated successfully"
}
```

**Error Response:**
```json
{
  "success": false,
  "error": "Phone number must be in international format",
  "phone_number": "+15551234567"
}
```

## Phone Number Format

- ✅ **Required**: International format with country code
- ✅ **Example**: `+15551234567` (US number)
- ✅ **Example**: `+447123456789` (UK number)
- ❌ **Invalid**: `5551234567` (missing country code)
- ❌ **Invalid**: `15551234567` (missing + prefix)

## Testing the Integration

### 1. Test with cURL:
```bash
curl -X POST "http://127.0.0.1:8000/call" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "phone_number=+15551234567&message=Test from cURL"
```

### 2. Test with Python:
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/call",
    data={
        "phone_number": "+15551234567",
        "message": "Test from Python"
    }
)

print(response.json())
```

### 3. Test Health Check:
```bash
curl http://127.0.0.1:8000/health
```

## Production Considerations

For production use with Cortex.ai:

1. **SSL/TLS**: Use HTTPS instead of HTTP
2. **Authentication**: Consider adding API key authentication
3. **Rate Limiting**: Implement rate limiting to prevent abuse
4. **Logging**: Enable detailed logging for debugging
5. **Error Handling**: Set up proper error notifications

## Troubleshooting

### Common Issues:

1. **CORS Errors**: 
   - Server includes `Access-Control-Allow-Origin: *` headers
   - If still having issues, check browser developer tools

2. **Phone Number Format**:
   - Always use international format with `+` prefix
   - Include country code (e.g., `+1` for US/Canada)

3. **Connection Refused**:
   - Ensure DocAlert server is running on port 8000
   - Check firewall settings if accessing remotely

4. **Twilio Errors**:
   - Verify Twilio credentials in `.env` file
   - Check Twilio account balance and phone number verification

## Support

For integration support:
- Check server logs for detailed error messages
- Use `/health` endpoint to verify service status
- Test with simple cURL commands first
- Verify phone number format and Twilio credentials
