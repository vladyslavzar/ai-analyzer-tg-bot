# Quick Test Reference

## Run Unit Tests - Quick Commands

### Basic Test Run
```bash
# Set environment variable and run all tests
TELEGRAM_BOT_TOKEN=test_token pytest -v
```

### Alternative: Create .env File
```bash
# Create a test .env file
echo "TELEGRAM_BOT_TOKEN=test_token_for_testing" > .env

# Run tests (they will use the .env file)
pytest -v
```

### Common Test Commands

```bash
# Run all tests with verbose output
TELEGRAM_BOT_TOKEN=test_token pytest -v

# Run with coverage report
TELEGRAM_BOT_TOKEN=test_token pytest --cov=app --cov-report=term-missing

# Run specific test file
TELEGRAM_BOT_TOKEN=test_token pytest tests/test_text_handler.py -v

# Show print statements during tests
TELEGRAM_BOT_TOKEN=test_token pytest -v -s

# Stop on first failure
TELEGRAM_BOT_TOKEN=test_token pytest -x

# Show test collection only (don't run)
TELEGRAM_BOT_TOKEN=test_token pytest --collect-only
```

## First Time Setup

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Create .env file with test token
echo "TELEGRAM_BOT_TOKEN=test_token_for_testing" > .env

# 3. Run tests
pytest -v
```

## For More Information

See [TESTING.md](TESTING.md) for comprehensive testing documentation.
