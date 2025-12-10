"""Tests for LLM handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from telegram import Update, Message, User, Chat
from telegram.ext import ContextTypes

from app.handlers.llm_text import handle_llm_request


@pytest.fixture
def mock_update():
    """Create a mock Telegram update."""
    user = User(id=123, first_name="Test", is_bot=False, username="testuser")
    chat = Chat(id=456, type="private")
    message = Message(
        message_id=1,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        text="/analyze Test text to analyze",
    )
    update = Update(update_id=1, message=message)
    return update


@pytest.fixture
def mock_context():
    """Create a mock context."""
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    return context


@pytest.mark.asyncio
async def test_handle_llm_request_with_text(mock_update, mock_context):
    """Test LLM analysis request with text."""
    mock_update.message.text = "/analyze This is a test message to analyze"
    mock_update.message.reply_text = AsyncMock(return_value=MagicMock())
    mock_update.message.reply_text.return_value.edit_text = AsyncMock()

    analysis_result = {
        "summary": "Test summary of the message",
        "tasks": ["Complete task 1"],
        "sentiment": "neutral",
    }

    with patch("app.handlers.llm_text.analyze_text", new_callable=AsyncMock) as mock_analyze, patch(
        "app.handlers.llm_text.log_event", new_callable=AsyncMock
    ):
        mock_analyze.return_value = analysis_result

        await handle_llm_request(mock_update, mock_context)

        # Should call analyze_text
        mock_analyze.assert_called_once()
        # Should send processing message
        assert mock_update.message.reply_text.called


@pytest.mark.asyncio
async def test_handle_llm_request_no_text(mock_update, mock_context):
    """Test LLM analysis request without text."""
    mock_update.message.text = "/analyze"
    mock_update.message.reply_text = AsyncMock()

    await handle_llm_request(mock_update, mock_context)

    # Should ask for text
    mock_update.message.reply_text.assert_called_once()


@pytest.mark.asyncio
async def test_handle_llm_request_empty_text(mock_update, mock_context):
    """Test LLM analysis request with empty text."""
    mock_update.message.text = "/analyze   "
    mock_update.message.reply_text = AsyncMock()

    await handle_llm_request(mock_update, mock_context)

    # Should ask for text
    assert mock_update.message.reply_text.called


