# Deploy Maharashtra AI Governance Platform on Render

## Step 1: Push to GitHub First
```bash
git add .
git commit -m "Add Render deployment files"
git push origin main
```

## Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub account
3. Connect your GitHub account

## Step 3: Deploy on Render
1. Click "New +" → "Web Service"
2. Connect your GitHub repository: `maharashtra-ai-governance`
3. Configure deployment:
   - **Name**: `maharashtra-ai-governance`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run working_dashboard.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

## Step 4: Environment Variables
Add these in Render dashboard:
- `GEMINI_API_KEY`: `AIzaSyBC52YIcFBSaQg4py6vJ6FhNCQEcONHMAg`
- `GOOGLE_CLOUD_PROJECT`: `maharashtra-governance`

## Step 5: Deploy
1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your app will be live at: `https://maharashtra-ai-governance.onrender.com`

## Features Available:
✅ Executive Dashboard
✅ AI Service Engine (with Gemini)
✅ Predictive Analytics
✅ Citizen Insights
✅ Security Monitoring

## Free Tier Limitations:
- App sleeps after 15 minutes of inactivity
- 750 hours/month free
- Slower cold starts

Your Maharashtra AI Governance Platform will be live on the internet! 🚀