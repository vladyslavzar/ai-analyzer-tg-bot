# Project Analysis Summary

## Overview

This is a **Telegram Bot with AI Features** built for university coursework. It's a production-ready bot that combines:
- Telegram bot functionality (text and image handling)
- AI-powered text analysis using LLM APIs
- Image classification using ResNet18
- FastAPI webhook server
- n8n integration for event logging

## Technology Stack

- **Language**: Python 3.11+
- **Web Framework**: FastAPI
- **Bot Framework**: python-telegram-bot (v20.7+)
- **AI/ML**: 
  - PyTorch & TorchVision (image classification)
  - Transformers library (LLM integration)
  - OpenRouter/OpenAI API (text analysis)
- **Testing**: pytest with pytest-asyncio
- **Code Quality**: Ruff (linting and formatting)

## Project Structure

```
ai-analyzer-tg-bot/
├── app/                        # Main application code
│   ├── handlers/               # Telegram message handlers
│   │   ├── text.py            # Text message handling
│   │   ├── image.py           # Image classification
│   │   └── llm_text.py        # LLM analysis
│   ├── utils/                  # Utility functions
│   │   ├── classify.py        # Image classification logic
│   │   ├── llm.py             # LLM API integration
│   │   └── events.py          # n8n event logging
│   ├── main.py                # FastAPI application
│   ├── bot.py                 # Bot setup
│   └── config.py              # Configuration management
├── tests/                      # Unit tests
│   ├── test_text_handler.py
│   ├── test_image_handler.py
│   └── test_llm_handler.py
├── pyproject.toml             # Dependencies and config
├── Dockerfile                 # Docker configuration
├── README.md                  # Main documentation
├── TESTING.md                 # Testing guide (NEW)
└── TESTING_QUICK_START.md     # Quick test reference (NEW)
```

## Key Features

1. **Text Message Handling**
   - Short messages: Simple echo response
   - Long messages (>200 chars): AI analysis with summary, tasks, and sentiment

2. **Image Classification**
   - Upload image → get predicted label with confidence score
   - Uses pre-trained ResNet18 model

3. **AI Text Analysis**
   - Concise 2-3 sentence summaries
   - Extracted actionable tasks/to-dos
   - Sentiment analysis (positive/neutral/negative)

4. **Webhook Integration**
   - FastAPI endpoint for Telegram webhooks
   - n8n event logging for automation workflows

## How to Run Unit Tests

### Quick Start

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Set environment variable and run tests
TELEGRAM_BOT_TOKEN=test_token pytest -v
```

### Alternative with .env File

```bash
# 1. Create .env file
echo "TELEGRAM_BOT_TOKEN=test_token" > .env

# 2. Run tests
pytest -v
```

### Common Test Commands

```bash
# Run all tests with verbose output
TELEGRAM_BOT_TOKEN=test_token pytest -v

# Run with coverage report
TELEGRAM_BOT_TOKEN=test_token pytest --cov=app --cov-report=html

# Run specific test file
TELEGRAM_BOT_TOKEN=test_token pytest tests/test_text_handler.py -v

# Show only test collection (don't run)
TELEGRAM_BOT_TOKEN=test_token pytest --collect-only
```

## Test Status

✅ **Test Infrastructure**: Fully configured and working
✅ **Test Discovery**: 8 tests successfully discovered
✅ **Dependencies**: All packages install correctly
⚠️ **Test Execution**: Tests have implementation issues (frozen Telegram objects)

### Current Tests

- **Text Handler** (3 tests): Short messages, long messages, no text
- **Image Handler** (2 tests): Successful classification, error handling
- **LLM Handler** (3 tests): With text, no text, empty text

## Important Notes

1. **Environment Variables Required**:
   - Tests need `TELEGRAM_BOT_TOKEN` set (can be dummy value)
   - Application loads config at import time
   - Use `.env` file or environment variable

2. **Known Test Issues**:
   - Tests try to modify frozen Telegram objects
   - Need refactoring to create objects with correct values at initialization
   - Framework is correct, fixtures need updating

3. **Documentation**:
   - `README.md` - Complete project documentation
   - `TESTING.md` - Comprehensive testing guide
   - `TESTING_QUICK_START.md` - Quick command reference

## Deployment Options

The project supports multiple deployment platforms:
- **Docker**: Dockerfile included
- **Render**: render.yaml configuration
- **Railway**: railway.json configuration
- **Manual**: Can run with uvicorn directly

## Code Quality Tools

```bash
# Run linter
ruff check .

# Auto-fix issues
ruff check --fix .

# Format code
ruff format .
```

## For University Submission

This project demonstrates:
- ✅ Modern Python web development (FastAPI)
- ✅ Asynchronous programming (async/await)
- ✅ AI/ML integration (PyTorch, LLM APIs)
- ✅ Testing practices (pytest, mocking)
- ✅ Configuration management (Pydantic settings)
- ✅ API integration (Telegram, OpenRouter, n8n)
- ✅ Deployment readiness (Docker, cloud platforms)
- ✅ Code quality practices (linting, type hints)

## Getting Help

- **Testing Issues**: See [TESTING.md](TESTING.md)
- **Quick Commands**: See [TESTING_QUICK_START.md](TESTING_QUICK_START.md)
- **General Setup**: See [README.md](README.md)
- **Troubleshooting**: Check README.md troubleshooting section

## Summary

The project is well-structured with:
- Clean architecture (handlers, utils separation)
- Comprehensive documentation
- Test infrastructure in place
- Multiple deployment options
- Professional code quality standards

**To run tests**: Simply install dependencies and use `TELEGRAM_BOT_TOKEN=test_token pytest -v`

For detailed information, refer to the new `TESTING.md` guide created specifically to help with running unit tests.
