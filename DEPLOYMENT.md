# Deployment Guide

This guide will walk you through deploying your Telegram bot to Render or Railway.

## 🚀 Deployment to Render

### Prerequisites
- A GitHub/GitLab/Bitbucket account with your bot code
- A Render account (sign up at https://render.com)

### Step-by-Step Instructions

#### 1. Push Your Code to GitHub
```bash
# Initialize git if not already done
git init
git add .
git commit -m "Initial commit: Telegram bot with AI features"

# Create a repository on GitHub, then:
git remote add origin https://github.com/yourusername/your-repo-name.git
git branch -M main
git push -u origin main
```

#### 2. Create a Render Account
1. Go to https://render.com
2. Sign up (free tier available)
3. Connect your GitHub account

#### 3. Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your repository
3. Render will automatically detect `render.yaml`

#### 4. Configure the Service
- **Name**: `telegram-bot` (or your preferred name)
- **Region**: Choose closest to you
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or `.` if needed)
- **Environment**: `Python 3`
- **Build Command**: `pip install uv && uv pip install -e .` (auto-detected from render.yaml)
- **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (auto-detected)

#### 5. Set Environment Variables
In the Render dashboard, go to **Environment** tab and add:

**Required:**
```
TELEGRAM_BOT_TOKEN=7872434684:AAET0vJDnBaxI7-j9BuWOPP-Uk-NKKTti9I
TELEGRAM_WEBHOOK_URL=https://your-service-name.onrender.com
TELEGRAM_SECRET_TOKEN=your_secret_token_here
```

**Optional (for AI features):**
```
LLM_API_KEY=your_openrouter_api_key
LLM_API_BASE=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo
N8N_WEBHOOK_URL=your_n8n_webhook_url
```

**Auto-configured:**
```
HOST=0.0.0.0
PORT=(automatically set by Render)
```

#### 6. Deploy!
1. Click **"Create Web Service"**
2. Wait for build to complete (5-10 minutes first time)
3. Copy your service URL (e.g., `https://telegram-bot-xyz.onrender.com`)

#### 7. Update Webhook URL
After deployment, update `TELEGRAM_WEBHOOK_URL` in Render with your actual service URL:
```
TELEGRAM_WEBHOOK_URL=https://telegram-bot-xyz.onrender.com
```

The bot will automatically set the webhook on startup!

### Render Free Tier Notes
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- For production, consider paid plans for always-on service

---

## 🚂 Deployment to Railway

### Prerequisites
- A GitHub account with your bot code
- A Railway account (sign up at https://railway.app)

### Step-by-Step Instructions

#### 1. Push Your Code to GitHub
(Same as Render step 1)

#### 2. Create a Railway Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Railway will automatically connect to your GitHub

#### 3. Create a New Project
1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository

#### 4. Railway Auto-Detection
Railway will automatically detect:
- `Dockerfile` → Uses Docker build
- `railway.json` → Uses configuration from file
- Python project → Sets up Python environment

#### 5. Configure Environment Variables
In Railway dashboard, go to **Variables** tab and add:

**Required:**
```
TELEGRAM_BOT_TOKEN=7872434684:AAET0vJDnBaxI7-j9BuWOPP-Uk-NKKTti9I
TELEGRAM_WEBHOOK_URL=https://your-service-name.up.railway.app
TELEGRAM_SECRET_TOKEN=your_secret_token_here
```

**Optional:**
```
LLM_API_KEY=your_openrouter_api_key
LLM_API_BASE=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo
N8N_WEBHOOK_URL=your_n8n_webhook_url
```

#### 6. Deploy!
1. Railway will automatically start building
2. Wait for deployment (3-5 minutes)
3. Get your service URL from the **Settings** → **Domains** section

#### 7. Update Webhook URL
After deployment, update `TELEGRAM_WEBHOOK_URL` in Railway with your actual domain:
```
TELEGRAM_WEBHOOK_URL=https://your-service-name.up.railway.app
```

### Railway Free Tier Notes
- $5 free credit monthly
- Services run continuously
- Auto-deploys on git push

---

## 🔧 Post-Deployment Checklist

### 1. Verify Webhook is Set
Check your bot's webhook status:
```bash
curl https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo
```

You should see:
```json
{
  "ok": true,
  "result": {
    "url": "https://your-service.onrender.com/webhook",
    "has_custom_certificate": false,
    "pending_update_count": 0
  }
}
```

### 2. Test Your Bot
1. Open Telegram
2. Find your bot: `@very_smart_analyzer_bot`
3. Send `/start`
4. Send a test message
5. Send a test image

### 3. Check Logs
- **Render**: Dashboard → Logs tab
- **Railway**: Dashboard → Deployments → View logs

### 4. Monitor Health
Check health endpoint:
```bash
curl https://your-service.onrender.com/health
```

Should return: `{"status": "healthy"}`

---

## 🐛 Troubleshooting

### Bot Not Responding
1. **Check webhook URL**: Make sure `TELEGRAM_WEBHOOK_URL` matches your service URL
2. **Check logs**: Look for errors in deployment logs
3. **Verify token**: Ensure `TELEGRAM_BOT_TOKEN` is correct
4. **Check service status**: Make sure service is running (not sleeping)

### Build Failures
1. **Python version**: Ensure using Python 3.11+ (check `pyproject.toml`)
2. **Dependencies**: Check if all dependencies are in `pyproject.toml`
3. **Build logs**: Review build logs for specific errors

### SSL Certificate Errors
- Render and Railway provide SSL certificates automatically
- Make sure you're using HTTPS in `TELEGRAM_WEBHOOK_URL`

### Service Keeps Restarting
1. Check application logs for errors
2. Verify all required environment variables are set
3. Check if port is correctly configured (should use `$PORT`)

---

## 📊 Quick Comparison

| Feature | Render | Railway |
|---------|--------|---------|
| Free Tier | ✅ (with limitations) | ✅ ($5 credit/month) |
| Always On | ❌ (spins down) | ✅ |
| Auto-Deploy | ✅ | ✅ |
| Custom Domain | ✅ | ✅ |
| SSL Certificate | ✅ | ✅ |
| Build Time | 5-10 min | 3-5 min |
| Cold Start | ~30s | Instant |

---

## 🔐 Security Best Practices

1. **Never commit `.env` file** - Already in `.gitignore`
2. **Use strong `TELEGRAM_SECRET_TOKEN`** - Generate a random string
3. **Rotate tokens regularly** - Especially if exposed
4. **Monitor logs** - Watch for suspicious activity
5. **Use HTTPS only** - Both platforms provide this automatically

---

## 🎯 Next Steps

After successful deployment:

1. ✅ Test all bot features
2. ✅ Set up monitoring/alerting
3. ✅ Configure n8n webhook (if using)
4. ✅ Add LLM API key for AI features
5. ✅ Set up custom domain (optional)
6. ✅ Enable auto-scaling (if needed)

---

## 📞 Need Help?

- **Render Docs**: https://render.com/docs
- **Railway Docs**: https://docs.railway.app
- **Telegram Bot API**: https://core.telegram.org/bots/api

Your bot is now ready for production! 🚀

