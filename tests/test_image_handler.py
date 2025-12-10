"""Tests for image message handler."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

from telegram import Update, Message, User, Chat, PhotoSize
from telegram.ext import ContextTypes

from app.handlers.image import handle_image_message


@pytest.fixture
def mock_update():
    """Create a mock Telegram update with photo."""
    user = User(id=123, first_name="Test", is_bot=False, username="testuser")
    chat = Chat(id=456, type="private")
    photo = [PhotoSize(file_id="test_file_id", width=100, height=100, file_unique_id="unique")]
    message = Message(
        message_id=1,
        date=datetime.now(),
        chat=chat,
        from_user=user,
        photo=photo,
    )
    update = Update(update_id=1, message=message)
    return update


@pytest.fixture
def mock_context():
    """Create a mock context with bot."""
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.bot.get_file = AsyncMock()
    mock_file = MagicMock()
    mock_file.download_as_bytearray = AsyncMock(return_value=b"fake_image_data")
    context.bot.get_file.return_value = mock_file
    return context


@pytest.mark.asyncio
async def test_handle_image_message_success(mock_update, mock_context):
    """Test successful image classification."""
    mock_update.message.reply_text = AsyncMock(return_value=MagicMock())
    mock_update.message.reply_text.return_value.edit_text = AsyncMock()

    with patch("app.handlers.image.classify_image") as mock_classify, patch(
        "app.handlers.image.log_event", new_callable=AsyncMock
    ) as mock_log:
        mock_classify.return_value = [("cat", 0.95), ("dog", 0.03), ("bird", 0.02)]

        await handle_image_message(mock_update, mock_context)

        # Should classify the image
        mock_classify.assert_called_once()
        # Should send processing message
        assert mock_update.message.reply_text.called
        # Should log event
        assert mock_log.called


@pytest.mark.asyncio
async def test_handle_image_message_error(mock_update, mock_context):
    """Test image handling with classification error."""
    mock_update.message.reply_text = AsyncMock(return_value=MagicMock())
    mock_update.message.reply_text.return_value.edit_text = AsyncMock()

    with patch("app.handlers.image.classify_image") as mock_classify, patch(
        "app.handlers.image.log_event", new_callable=AsyncMock
    ):
        mock_classify.side_effect = ValueError("Classification failed")

        await handle_image_message(mock_update, mock_context)

        # Should handle error gracefully
        assert True

