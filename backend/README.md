# DocAlert API

A comprehensive FastAPI-based service for sending voice alerts and SMS notifications using Twilio, with advanced features like voicemail support and automatic fallbacks.

## Features

- 📞 **Voice Calls** with custom messages
- 🎙️ **Voicemail Support** - Enhanced TwiML for voicemail scenarios
- 📱 **SMS Messaging** 
- 🔄 **Unified Notifications** - Send both SMS and calls
- 💪 **Smart Fallbacks** - Automatic SMS if calls fail
- 🏥 **Health Monitoring** - Service status endpoints
- 📚 **Auto Documentation** - Swagger UI included

## Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Variables**
   Create a `.env` file in the backend directory with:
   ```
   TWILIO_ACCOUNT_SID=your_twilio_account_sid
   TWILIO_AUTH_TOKEN=your_twilio_auth_token
   TWILIO_FROM_NUMBER=+1234567890
   TEST_PHONE_NUMBER=+1234567890
   ```

3. **Run the Server**
   ```bash
   python main.py
   ```
   
   The server will start on `http://127.0.0.1:8000`

## API Endpoints

### Health & Status
- **GET** `/health` - Check service status and configuration
- **GET** `/` - Basic health check

### Voice Calls
- **POST** `/make-call` - Make a phone call with enhanced features
  ```json
  {
    "to_number": "+15551234567",
    "message": "Your custom message here",
    "callback_url": "optional_webhook_url",
    "enable_voicemail": true,
    "fallback_to_sms": false
  }
  ```

### SMS Messaging  
- **POST** `/send-sms` - Send SMS message
  ```json
  {
    "to_number": "+15551234567", 
    "message": "Your SMS message here"
  }
  ```

### Unified Notifications
- **POST** `/send-notification` - Send via SMS, call, or both
  ```json
  {
    "to_number": "+15551234567",
    "message": "Your notification message",
    "method": "both",
    "enable_voicemail": true
  }
  ```

### Testing Endpoints
- **POST** `/test-call` - Test call with voicemail & SMS fallback
- **POST** `/test-sms` - Test SMS to configured number  
- **POST** `/test-notification` - Test unified notification

### Webhooks
- **POST** `/twiml` - TwiML webhook for custom call flows

### Documentation
- **GET** `/docs` - Interactive API documentation (Swagger UI)
- **GET** `/redoc` - Alternative API documentation

## Advanced Features

### Voicemail Support
When `enable_voicemail: true`, calls include:
- Longer message duration
- Message repetition for clarity
- Voicemail-friendly pacing
- Professional greeting and closing

### Smart SMS Fallback
When `fallback_to_sms: true`:
- Monitors call status automatically
- Sends SMS if call fails/busy/no-answer
- Includes context about missed call
- Works seamlessly in background

### Unified Notifications
The `/send-notification` endpoint allows:
- `method: "sms"` - SMS only
- `method: "call"` - Call only (with SMS fallback option)
- `method: "both"` - Both SMS and call simultaneously

## Example Usage

### Python Examples

#### Simple Call
```python
import requests

response = requests.post("http://127.0.0.1:8000/make-call", json={
    "to_number": "+15551234567",
    "message": "Hello! This is an alert from DocAlert.",
    "enable_voicemail": True,
    "fallback_to_sms": True
})

print(response.json())
```

#### Send SMS
```python
response = requests.post("http://127.0.0.1:8000/send-sms", json={
    "to_number": "+15551234567", 
    "message": "📱 Important alert: Your appointment is in 30 minutes."
})
```

#### Unified Notification
```python
response = requests.post("http://127.0.0.1:8000/send-notification", json={
    "to_number": "+15551234567",
    "message": "Critical system alert: Server maintenance in 15 minutes",
    "method": "both",
    "enable_voicemail": True
})
```

### cURL Examples

#### Call with Voicemail
```bash
curl -X POST "http://127.0.0.1:8000/make-call" \
     -H "Content-Type: application/json" \
     -d '{
       "to_number": "+15551234567",
       "message": "Emergency alert from DocAlert system",
       "enable_voicemail": true,
       "fallback_to_sms": true
     }'
```

#### SMS Message
```bash
curl -X POST "http://127.0.0.1:8000/send-sms" \
     -H "Content-Type: application/json" \
     -d '{
       "to_number": "+15551234567",
       "message": "Your DocAlert notification via SMS"
     }'
```

## Testing

Run the comprehensive test suite:
```bash
python test_api.py
```

The test script will:
- Check service health
- Test all predefined endpoints
- Allow custom interactive testing
- Validate all features

## Response Format

All endpoints return detailed responses:

```json
{
  "success": true,
  "call_sid": "CAxxxx...",
  "sms_sid": "SMxxxx...", 
  "message": "Status message",
  "actions_taken": ["call_initiated", "sms_fallback_sent"],
  "errors": []
}
```

## Error Handling

Comprehensive error handling includes:
- Phone number format validation
- Twilio credential verification
- API rate limit handling
- Network connectivity issues
- Detailed error messages with HTTP status codes

## Security & Best Practices

- ✅ Environment variables for all secrets
- ✅ Input validation and sanitization  
- ✅ Phone number format verification
- ✅ Message length limits (SMS: 1600 chars)
- ✅ Comprehensive logging
- ✅ Error handling without exposing internals

## Twilio Configuration

1. Sign up at https://www.twilio.com
2. Get Account SID and Auth Token from Console
3. Purchase a phone number for outbound calls/SMS
4. Add credentials to `.env` file
5. Verify phone numbers for testing (if using trial account)

## Production Considerations

- Implement API authentication (JWT, API keys)
- Add rate limiting for endpoints
- Set up proper logging and monitoring
- Use HTTPS in production
- Configure webhook URLs for advanced TwiML
- Consider message queuing for high volume
- Implement retry logic for failed notifications

## Troubleshooting

### Common Issues

1. **"Twilio service not configured"**
   - Check `.env` file exists and has correct values
   - Verify environment variables are loaded

2. **"Phone number must be in international format"** 
   - Use format: `+1234567890` (include country code)

3. **SMS/Call fails**
   - Verify Twilio account has sufficient balance
   - Check if destination number is verified (trial accounts)
   - Ensure FROM number is a valid Twilio number

4. **Voicemail not working as expected**
   - Test with different carriers (behavior varies)
   - Consider webhook-based TwiML for more control
