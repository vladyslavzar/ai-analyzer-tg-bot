# Local Testing Guide

This guide will help you test the Telegram bot locally using polling mode (no webhook needed).

## 🚀 Quick Start

### Step 1: Get a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token (looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Create .env File

Create a `.env` file in the project root:

```bash
# Copy the example (if it exists) or create new
touch .env
```

Add your bot token to `.env`:

```env
# Required for local testing
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional - leave empty for polling mode
TELEGRAM_WEBHOOK_URL=

# Optional - for AI features
LLM_API_KEY=your_openrouter_key_here
LLM_API_BASE=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo

# Optional - for n8n integration
N8N_WEBHOOK_URL=

# Server config (not needed for polling)
HOST=0.0.0.0
PORT=8000
```

### Step 3: Install Dependencies

```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install project dependencies
uv pip install -e .
```

### Step 4: Run the Bot in Polling Mode

```bash
python run_polling.py
```

You should see:
```
============================================================
Starting Telegram Bot in POLLING mode
============================================================
Bot token: 1234567890...
Press Ctrl+C to stop the bot
============================================================
✅ Bot is running and polling for updates...
   Send a message to your bot on Telegram to test it!
```

### Step 5: Test on Telegram

1. Open Telegram and search for your bot (the username you gave it)
2. Click "Start" or send `/start`
3. Try these tests:

**Test 1: Short Text Message**
- Send: `Hello`
- Expected: Bot replies with "You said: Hello"

**Test 2: Long Text Message (AI Analysis)**
- Send a message longer than 200 characters, for example:
  ```
  I need to finish my project by next week. I should research the requirements, 
  create design mockups, implement the core features, write tests, and deploy 
  to production. I'm feeling confident about the timeline and excited to get started!
  ```
- Expected: Bot analyzes and returns summary, tasks, and sentiment

**Test 3: Image Classification**
- Send any photo/image
- Expected: Bot classifies the image and returns a label with confidence

**Test 4: Commands**
- Send `/start` - Shows welcome message
- Send `/help` - Shows help message

## 🧪 Running Unit Tests

Test the code without needing a real bot:

```bash
# Install test dependencies
uv pip install -e ".[dev]"

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_text_handler.py -v
```

## 🔍 Testing Individual Components

### Test FastAPI Server (Webhook Mode)

If you want to test the webhook endpoint:

```bash
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

In another terminal, test the endpoints:

```bash
# Health check
curl http://localhost:8000/health

# Root endpoint
curl http://localhost:8000/

# Test events/log endpoint
curl -X POST http://localhost:8000/events/log \
  -H "Content-Type: application/json" \
  -d '{"event_type": "test", "data": {"test": "data"}}'
```

## 🐛 Troubleshooting

### "TELEGRAM_BOT_TOKEN is not set"
- Make sure you created a `.env` file
- Check that `TELEGRAM_BOT_TOKEN=your_token` is in the file
- Verify there are no spaces around the `=` sign

### "Module not found" errors
- Run: `uv pip install -e .`
- Make sure you're in the project directory

### Bot doesn't respond
- Check that the bot token is correct
- Make sure you've started the bot with `/start` in Telegram
- Check the console logs for errors

### AI features not working
- Make sure `LLM_API_KEY` is set in `.env`
- Check that you have credits/access to the LLM API
- For OpenRouter, sign up at https://openrouter.ai

### Image classification fails
- First run will download the ResNet18 model (~45MB) - be patient
- Make sure you have internet connection
- Check that the image format is supported (JPEG, PNG)

## 📝 Testing Checklist

- [ ] Bot token obtained from BotFather
- [ ] `.env` file created with `TELEGRAM_BOT_TOKEN`
- [ ] Dependencies installed (`uv pip install -e .`)
- [ ] Bot runs without errors (`python run_polling.py`)
- [ ] Can send `/start` and receive response
- [ ] Short text messages are echoed
- [ ] Long text messages trigger AI analysis (if LLM_API_KEY set)
- [ ] Image classification works (sends photo, gets label)
- [ ] Unit tests pass (`pytest`)

## 🎯 Next Steps

Once local testing works:
1. Test with real LLM API key for AI features
2. Set up n8n webhook for event logging
3. Deploy to Render/Railway for production
4. Configure webhook URL for production deployment


