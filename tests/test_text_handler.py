"""Tests for text message handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.handlers.text import handle_text_message, LONG_TEXT_THRESHOLD


@pytest.fixture
def mock_update():
    """Create a mock Telegram update."""
    update = MagicMock()
    update.message = MagicMock()
    update.message.text = "Test message"
    update.message.reply_text = AsyncMock(return_value=MagicMock())
    update.message.reply_text.return_value.edit_text = AsyncMock()
    return update


@pytest.fixture
def mock_context():
    """Create a mock context."""
    context = MagicMock()
    return context


@pytest.mark.asyncio
async def test_handle_short_text_message(mock_update, mock_context):
    """Test handling of short text messages."""
    mock_update.message.text = "Hello"

    with patch("app.handlers.text.log_event", new_callable=AsyncMock) as mock_log:
        await handle_text_message(mock_update, mock_context)

        # Should send a response
        assert mock_update.message.reply_text.called
        # Should log event
        assert mock_log.called
        # Verify greeting response
        call_args = mock_update.message.reply_text.call_args
        assert "Hello" in call_args[0][0] or "hello" in call_args[0][0].lower()


@pytest.mark.asyncio
async def test_handle_long_text_message(mock_update, mock_context):
    """Test handling of long text messages with AI analysis."""
    # Create a long message
    long_text = "A" * (LONG_TEXT_THRESHOLD + 1)
    mock_update.message.text = long_text

    analysis_result = {
        "summary": "Test summary",
        "tasks": ["Task 1", "Task 2"],
        "sentiment": "positive",
    }

    with patch("app.handlers.text.log_event", new_callable=AsyncMock), \
        patch("app.handlers.text.analyze_text", new_callable=AsyncMock) as mock_analyze:
        mock_analyze.return_value = analysis_result

        await handle_text_message(mock_update, mock_context)

        # Should call analyze_text
        mock_analyze.assert_called_once_with(long_text)
        # Should send processing message
        assert mock_update.message.reply_text.called


@pytest.mark.asyncio
async def test_handle_text_message_no_text(mock_update, mock_context):
    """Test handling update with no text message."""
    mock_update.message.text = None

    with patch("app.handlers.text.log_event", new_callable=AsyncMock):
        await handle_text_message(mock_update, mock_context)

        # Should not raise error
        assert True



