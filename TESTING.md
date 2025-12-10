# Testing Guide

This document provides comprehensive instructions for running and understanding the unit tests in this project.

## Overview

The project uses **pytest** as the testing framework with **pytest-asyncio** for testing asynchronous functions. The tests are located in the `tests/` directory and cover the main handler functions for text, image, and LLM analysis.

## Test Structure

```
tests/
├── __init__.py
├── test_text_handler.py      # Tests for text message handling
├── test_image_handler.py     # Tests for image classification
└── test_llm_handler.py        # Tests for LLM analysis
```

## Prerequisites

Before running tests, ensure you have:

1. **Python 3.11+** installed
2. **Project dependencies** installed (including dev dependencies)

## Installation

### Option 1: Using pip (Recommended)

Install the project with development dependencies:

```bash
pip install -e ".[dev]"
```

This will install:
- Main dependencies (FastAPI, python-telegram-bot, torch, etc.)
- Testing dependencies (pytest, pytest-asyncio)
- Linting tools (ruff)

### Option 2: Using uv (Fast Alternative)

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies
uv pip install -e ".[dev]"
```

## Environment Setup

The tests require a `TELEGRAM_BOT_TOKEN` environment variable to be set (even with a dummy value) because the application configuration is loaded at module import time.

### Set Environment Variable

**Linux/macOS:**
```bash
export TELEGRAM_BOT_TOKEN="test_token_for_testing"
```

**Windows (Command Prompt):**
```cmd
set TELEGRAM_BOT_TOKEN=test_token_for_testing
```

**Windows (PowerShell):**
```powershell
$env:TELEGRAM_BOT_TOKEN="test_token_for_testing"
```

## Running Tests

### Run All Tests

```bash
TELEGRAM_BOT_TOKEN=test_token pytest
```

Or with verbose output:

```bash
TELEGRAM_BOT_TOKEN=test_token pytest -v
```

### Run Specific Test File

```bash
TELEGRAM_BOT_TOKEN=test_token pytest tests/test_text_handler.py
```

### Run Specific Test Function

```bash
TELEGRAM_BOT_TOKEN=test_token pytest tests/test_text_handler.py::test_handle_short_text_message
```

### Run with Coverage

To see code coverage information:

```bash
TELEGRAM_BOT_TOKEN=test_token pytest --cov=app --cov-report=html
```

This generates an HTML coverage report in `htmlcov/index.html`.

### Run with Coverage (Terminal Report)

```bash
TELEGRAM_BOT_TOKEN=test_token pytest --cov=app --cov-report=term-missing
```

## Test Configuration

The test configuration is defined in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
```

This configuration:
- Sets `tests/` as the default test directory
- Automatically detects test files matching `test_*.py`
- Enables automatic asyncio mode for async tests

## Known Test Issues

### Current Status

⚠️ **Note**: The existing tests have some implementation issues:

1. **Frozen Telegram Objects**: The tests attempt to modify attributes on Telegram library objects (like `Message`), which are frozen and cannot be modified after creation.
2. **Test Fixture Issues**: The mock fixtures need to be refactored to properly create objects with the desired values at initialization time, rather than trying to modify them afterward.

### Example Issue

```python
# ❌ This fails because Message objects are frozen
mock_update.message.text = "Hello"

# ✅ This would work - create Message with text at initialization
message = Message(
    message_id=1,
    date=datetime.now(),
    chat=chat,
    from_user=user,
    text="Hello"  # Set during creation
)
```

### Running Tests Despite Issues

Even with these issues, you can see the test discovery and collection working:

```bash
TELEGRAM_BOT_TOKEN=test_token pytest --collect-only
```

This shows all tests that pytest can find without running them.

## Test Coverage

The current test suite covers:

### Text Handler Tests (`test_text_handler.py`)
- ✅ Short text messages (echo functionality)
- ✅ Long text messages (AI analysis)
- ✅ Messages with no text

### Image Handler Tests (`test_image_handler.py`)
- ✅ Successful image classification
- ✅ Image classification error handling

### LLM Handler Tests (`test_llm_handler.py`)
- ✅ LLM analysis with text
- ✅ LLM analysis with no text
- ✅ LLM analysis with empty text

## Writing New Tests

When writing new tests for this project:

1. **Use pytest fixtures** for common setup
2. **Mock external dependencies** (API calls, file I/O)
3. **Create Telegram objects properly** - pass all values during initialization
4. **Use AsyncMock** for async functions
5. **Follow the existing test structure**

### Example Test Template

```python
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes


@pytest.fixture
def mock_update():
    """Create a properly initialized mock update."""
    user = User(id=123, first_name="Test", is_bot=False, username="testuser")
    chat = Chat(id=456, type="private")
    message = Message(
        message_id=1,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text="Your test text here"  # Set during creation
    )
    update = Update(update_id=1, message=message)
    return update


@pytest.mark.asyncio
async def test_your_function(mock_update):
    """Test description."""
    # Your test code here
    pass
```

## Debugging Tests

### Run with Debug Output

```bash
TELEGRAM_BOT_TOKEN=test_token pytest -v -s
```

The `-s` flag shows print statements and logging output.

### Run with PDB Debugger

```bash
TELEGRAM_BOT_TOKEN=test_token pytest --pdb
```

This drops into the Python debugger on test failures.

### Show Local Variables on Failure

```bash
TELEGRAM_BOT_TOKEN=test_token pytest -l
```

## Integration with CI/CD

For continuous integration, you can:

1. **Set environment variables** in your CI configuration
2. **Run tests in Docker** using the provided Dockerfile
3. **Generate coverage reports** for tracking

### Example GitHub Actions Workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -e ".[dev]"
      - name: Run tests
        env:
          TELEGRAM_BOT_TOKEN: test_token
        run: pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Reinstall the package in editable mode
pip install -e .
```

### Missing Dependencies

If tests fail due to missing packages:
```bash
# Install dev dependencies
pip install -e ".[dev]"
```

### Environment Variable Not Set

If you see validation errors about `telegram_bot_token`:
```
ValidationError: 1 validation error for Settings
telegram_bot_token
  Field required
```

Make sure to set the environment variable:
```bash
export TELEGRAM_BOT_TOKEN=test_token
```

## Additional Resources

- [pytest documentation](https://docs.pytest.org/)
- [pytest-asyncio documentation](https://pytest-asyncio.readthedocs.io/)
- [python-telegram-bot testing guide](https://docs.python-telegram-bot.org/en/stable/testing.html)

## Summary

To quickly run tests on this project:

```bash
# 1. Install dependencies
pip install -e ".[dev]"

# 2. Set environment variable and run tests
TELEGRAM_BOT_TOKEN=test_token pytest -v

# 3. (Optional) Generate coverage report
TELEGRAM_BOT_TOKEN=test_token pytest --cov=app --cov-report=html
```

⚠️ **Note**: While the test infrastructure is in place, the current tests need refactoring to work with frozen Telegram objects. The tests are discoverable and the framework is correctly configured, but individual test cases will fail until the fixtures are properly updated.
