# Telegram Bot with AI Features

A production-ready Telegram bot built with Python, FastAPI, and python-telegram-bot. Features AI-powered text analysis, image classification, and n8n integration for automation workflows.

## 🚀 Features

- **Text Message Handling**: Responds to any text message
- **Image Classification**: Accepts images and returns predicted labels using ResNet18
- **AI Text Analysis**: For long messages (>200 chars), provides:
  - Concise AI summary
  - Extracted tasks/to-dos
  - Sentiment analysis (positive/neutral/negative)
- **FastAPI Webhook**: `/webhook` endpoint to receive Telegram updates
- **n8n Integration**: Event logging endpoint for automation workflows

## 📁 Project Structure

```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── bot.py               # Bot setup and configuration
│   ├── config.py            # Configuration management
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── text.py          # Text message handler
│   │   ├── image.py         # Image message handler
│   │   └── llm_text.py      # LLM-specific handler
│   └── utils/
│       ├── __init__.py
│       ├── classify.py      # Image classification
│       ├── llm.py           # LLM text analysis
│       └── events.py        # n8n event logging
├── tests/
│   ├── __init__.py
│   ├── test_text_handler.py
│   ├── test_image_handler.py
│   └── test_llm_handler.py
├── pyproject.toml           # Dependencies and config
├── Dockerfile               # Docker configuration
├── render.yaml              # Render deployment config
├── railway.json             # Railway deployment config
└── README.md
```

## 🛠️ Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenRouter API key (or any OpenAI-compatible API)

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd tgbot
   ```

2. **Install dependencies using uv**:
   ```bash
   # Install uv if not already installed
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies
   uv pip install -e .
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

### Environment Variables

Create a `.env` file with the following variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_WEBHOOK_URL=https://your-domain.com/webhook
TELEGRAM_SECRET_TOKEN=your_secret_token_here

# LLM Configuration (OpenRouter or OpenAI-compatible API)
LLM_API_KEY=your_openrouter_api_key_here
LLM_API_BASE=https://openrouter.ai/api/v1
LLM_MODEL=openai/gpt-3.5-turbo

# n8n Event Logging
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/events/log

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

## 🏃 Running Locally

### Development Mode

```bash
# Run with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Using Python directly

```bash
python -m app.main
```

The bot will start and automatically configure the webhook if `TELEGRAM_WEBHOOK_URL` is set.

## 🔧 Webhook Setup

### Setting up Telegram Webhook

The bot automatically sets up the webhook on startup if `TELEGRAM_WEBHOOK_URL` is configured. The webhook endpoint is:

```
POST /webhook
```

**Manual webhook setup** (if needed):

```bash
curl -X POST "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook" \
  -d "url=https://your-domain.com/webhook" \
  -d "secret_token=your_secret_token"
```

### Webhook Security

The webhook endpoint verifies the `X-Telegram-Bot-Api-Secret-Token` header if `TELEGRAM_SECRET_TOKEN` is configured. This prevents unauthorized access to your webhook.

## 🤖 How It Works

### Text Message Handling

1. **Short messages** (<200 chars): Simple echo response
2. **Long messages** (>200 chars): 
   - Sends "Analyzing..." message
   - Calls LLM API for analysis
   - Returns formatted response with:
     - Summary
     - Extracted tasks
     - Sentiment analysis

### Image Classification

1. User sends an image
2. Bot downloads the image
3. Processes with ResNet18 (ImageNet pre-trained)
4. Returns predicted label and confidence score

### AI Summarizer

The AI summarizer (`app/utils/llm.py`) uses an OpenAI-compatible API (default: OpenRouter) to:

1. **Generate Summary**: Creates a 2-3 sentence summary
2. **Extract Tasks**: Identifies actionable items/to-dos
3. **Analyze Sentiment**: Determines if message is positive, neutral, or negative

**Example AI Summary Output**:

```json
{
  "summary": "The user is planning a project with multiple tasks including research, design, and implementation. They're feeling positive about the timeline.",
  "tasks": [
    "Research project requirements",
    "Create design mockups",
    "Implement core features"
  ],
  "sentiment": "positive"
}
```

## 📊 n8n Integration

### Event Logging Endpoint

The bot sends events to the configured n8n webhook URL for each interaction:

- **Text messages**: `text_message` event
- **Image messages**: `image_message` event
- **LLM analysis**: `llm_analysis` event

### Example Event JSON

**Text Message Event**:
```json
{
  "event_type": "text_message",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "user_id": 123456789,
  "chat_id": 123456789,
  "data": {
    "message_text": "Hello, this is a test message",
    "message_length": 28
  }
}
```

**Image Message Event**:
```json
{
  "event_type": "image_message",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "user_id": 123456789,
  "chat_id": 123456789,
  "data": {
    "file_id": "AgACAgIAAxkBAAIB...",
    "prediction": {
      "label": "cat",
      "confidence": 95.3
    }
  }
}
```

**LLM Analysis Event**:
```json
{
  "event_type": "llm_analysis",
  "timestamp": "2024-01-15T10:30:00.000Z",
  "user_id": 123456789,
  "chat_id": 123456789,
  "data": {
    "original_text": "Long message text here...",
    "analysis": {
      "summary": "AI-generated summary",
      "tasks": ["Task 1", "Task 2"],
      "sentiment": "positive"
    }
  }
}
```

### n8n Workflow Setup

1. **Create a Webhook node** in n8n:
   - Method: POST
   - Path: `/webhook/events/log`
   - Authentication: None (or add your own)

2. **Configure the workflow** to process events:
   - Filter by `event_type`
   - Store data in database/notion/sheets
   - Send notifications
   - Trigger other automations

3. **Example n8n Workflow JSON**:

```json
{
  "name": "Telegram Bot Events",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "events/log",
        "responseMode": "responseNode"
      },
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "string": [
            {
              "value1": "={{$json.body.event_type}}",
              "operation": "equals",
              "value2": "text_message"
            }
          ]
        }
      },
      "name": "Filter Text Messages",
      "type": "n8n-nodes-base.if",
      "typeVersion": 1,
      "position": [450, 300]
    },
    {
      "parameters": {
        "operation": "append",
        "table": {
          "values": [
            {
              "column": "timestamp",
              "value": "={{$json.body.timestamp}}"
            },
            {
              "column": "event_type",
              "value": "={{$json.body.event_type}}"
            },
            {
              "column": "user_id",
              "value": "={{$json.body.user_id}}"
            }
          ]
        }
      },
      "name": "Store Event",
      "type": "n8n-nodes-base.googleSheets",
      "typeVersion": 1,
      "position": [650, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "Filter Text Messages", "type": "main", "index": 0}]]
    },
    "Filter Text Messages": {
      "main": [[{"node": "Store Event", "type": "main", "index": 0}]]
    }
  }
}
```

## 🧪 Testing

The project uses pytest for unit testing. Tests require a `TELEGRAM_BOT_TOKEN` environment variable to be set.

### Quick Start

```bash
# Install test dependencies
pip install -e ".[dev]"

# Run all tests
TELEGRAM_BOT_TOKEN=test_token pytest -v

# Run with coverage
TELEGRAM_BOT_TOKEN=test_token pytest --cov=app --cov-report=html

# Run specific test file
TELEGRAM_BOT_TOKEN=test_token pytest tests/test_text_handler.py
```

### Detailed Testing Guide

For comprehensive testing instructions, troubleshooting, and best practices, see [TESTING.md](TESTING.md).

The testing guide covers:
- Complete setup instructions
- Environment configuration
- Running tests with different options
- Writing new tests
- Known issues and solutions
- CI/CD integration examples

## 🐳 Docker Deployment

### Build and Run

```bash
# Build image
docker build -t telegram-bot .

# Run container
docker run -d \
  --name telegram-bot \
  -p 8000:8000 \
  --env-file .env \
  telegram-bot
```

## ☁️ Deployment

### Render

1. Connect your repository to Render
2. Create a new Web Service
3. Render will automatically detect `render.yaml`
4. Add environment variables in Render dashboard
5. Deploy!

The `render.yaml` file configures:
- Build command: `pip install uv && uv pip install -e .`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Environment variables

### Railway

1. Connect your repository to Railway
2. Railway will detect `railway.json` and `Dockerfile`
3. Add environment variables in Railway dashboard
4. Deploy!

The `railway.json` file configures:
- Docker build
- Start command
- Restart policy

### Environment Variables for Deployment

Make sure to set all required environment variables in your deployment platform:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_WEBHOOK_URL` (your deployed URL)
- `TELEGRAM_SECRET_TOKEN` (optional but recommended)
- `LLM_API_KEY`
- `LLM_API_BASE` (default: `https://openrouter.ai/api/v1`)
- `LLM_MODEL` (default: `openai/gpt-3.5-turbo`)
- `N8N_WEBHOOK_URL` (optional)

## 📝 Code Quality

### Linting

```bash
# Run ruff
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Formatting

```bash
# Format code with ruff
ruff format .
```

## 🔒 Security Notes

- Never commit `.env` file
- Use strong `TELEGRAM_SECRET_TOKEN` for webhook security
- Keep API keys secure
- Use HTTPS for webhook URLs
- Consider rate limiting for production

## 📚 Dependencies

- **FastAPI**: Web framework
- **python-telegram-bot**: Telegram Bot API wrapper
- **torch/torchvision**: Image classification
- **httpx**: Async HTTP client
- **pydantic**: Settings management
- **pytest**: Testing framework

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run linting and tests
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🆘 Troubleshooting

### Bot not responding

- Check that `TELEGRAM_BOT_TOKEN` is correct
- Verify webhook is set: `curl https://api.telegram.org/bot<TOKEN>/getWebhookInfo`
- Check application logs

### Image classification fails

- Ensure torch/torchvision are installed correctly
- Check image format is supported (JPEG, PNG)
- Verify sufficient memory for model loading

### LLM analysis not working

- Verify `LLM_API_KEY` is set and valid
- Check API endpoint is accessible
- Review API rate limits

### n8n events not received

- Verify `N8N_WEBHOOK_URL` is correct
- Check n8n webhook is active
- Review network connectivity

## 📞 Support

For issues and questions, please open an issue on the repository.


