# DocAlert - Render Deployment Guide

## 🚀 Quick Deploy to Render

### Prerequisites
✅ GitHub repository with your code  
✅ Twilio account with credentials  
✅ Render account (free tier works)

### Step 1: Prepare Your Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Create Web Service on Render
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Settings:**
- **Name**: `docalert-api`
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

### Step 3: Environment Variables
Add these in Render's Environment tab:
```
TWILIO_ACCOUNT_SID=your_account_sid_here
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_PHONE_NUMBER=your_twilio_phone_number
DOCALERT_API_KEY=your_generated_api_key_here
```

**⚠️ Important**: Use the API key generated from `python generate_api_key.py`

### Step 4: Deploy
- Click "Create Web Service"
- Render will automatically deploy from your GitHub repo
- First deployment takes 5-10 minutes

## 🔧 Your Deployment Files

### Files Created for Render:
- `Procfile` - Tells Render how to start your app
- `runtime.txt` - Specifies Python version
- `render.sh` - Optional build script
- `requirements.txt` - Already existed, lists dependencies

### API Endpoints After Deployment:
- **Health Check**: `https://your-app.onrender.com/health`
- **API Docs**: `https://your-app.onrender.com/docs`
- **Voice Call (JSON)**: `POST https://your-app.onrender.com/make-call`
- **Voice Call (Form)**: `POST https://your-app.onrender.com/call`
- **Test Call**: `POST https://your-app.onrender.com/test-call`

## 🧪 Testing Your Deployed API

### Using curl:
```bash
# Health check
curl https://your-app.onrender.com/health

# Make a call (replace with your URL and API key)
curl -X POST https://your-app.onrender.com/call \
  -H "X-API-Key: your_api_key_here" \
  -d "phone_number=+15551234567" \
  -d "message=Hello from DocAlert!"
```

### Using your test script:
```python
# Update BASE_URL in test_api.py
BASE_URL = "https://your-app.onrender.com"
```

## 🔄 Automatic Deployments
- Render automatically redeploys when you push to `main` branch
- Monitor deployments in Render dashboard
- View logs for debugging

## 💡 Production Tips

### Custom Domain (Optional):
- Add custom domain in Render settings
- Update CORS if needed for specific domains

### Monitoring:
- Use Render's built-in monitoring
- Check `/health` endpoint for uptime monitoring

### Scaling:
- Free tier: Limited hours/month
- Paid tiers: Unlimited with autoscaling

## 🤖 Cortex.ai Integration
Once deployed, use your Render URL in Cortex.ai:
```
Endpoint: https://your-app.onrender.com/call
Method: POST (Form Data)
Headers: X-API-Key: your_api_key_here
Fields: phone_number, message
```

## 🆘 Troubleshooting

### Common Issues:
1. **Build fails**: Check requirements.txt formatting
2. **App won't start**: Verify Procfile and start command
3. **Twilio errors**: Double-check environment variables
4. **CORS issues**: Already configured for all origins

### Debug Commands:
```bash
# Local test before deploy
python server.py

# Check logs in Render dashboard
# Environment → Logs tab
```

## 📱 Next Steps After Deployment
1. Test all endpoints work
2. Configure Cortex.ai with your new URL
3. Set up monitoring/alerts
4. Consider adding authentication for production use

Your DocAlert API will be live at `https://your-service-name.onrender.com`!
