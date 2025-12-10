"""Telegram bot setup and configuration."""

import logging
from typing import Any

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from app.config import settings
from app.handlers.image import handle_image_message
from app.handlers.text import handle_text_message

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def create_bot_application() -> Application:
    """
    Create and configure the Telegram bot application.

    Returns:
        Configured Application instance
    """
    application = Application.builder().token(settings.telegram_bot_token).build()

    # Register handlers
    # Text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_message))

    # Image messages
    application.add_handler(MessageHandler(filters.PHOTO, handle_image_message))

    # Start command
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    return application


async def start_command(update: Update, context: Any) -> None:
    """Handle /start command."""
    await update.message.reply_text(
        "👋 <b>Welcome! I'm your Smart AI Assistant Bot!</b>\n\n"
        "🤖 <b>What I can do:</b>\n\n"
        "📸 <b>Image Recognition:</b>\n"
        "   Send me any photo and I'll identify what's in it!\n"
        "   I'll show you the top 3 most likely objects.\n\n"
        "📝 <b>Text Analysis:</b>\n"
        "   • Short messages: Get word/character count\n"
        "   • Long messages (>200 chars): AI-powered analysis\n"
        "     - Generate summaries\n"
        "     - Extract tasks/to-dos\n"
        "     - Analyze sentiment\n\n"
        "🚀 <b>Try it now:</b>\n"
        "   • Send me a photo 📷\n"
        "   • Send a short message 💬\n"
        "   • Send a long message for AI analysis 🤖\n\n"
        "Type /help for more info!",
        parse_mode="HTML"
    )


async def help_command(update: Update, context: Any) -> None:
    """Handle /help command."""
    await update.message.reply_text(
        "📖 <b>Bot Commands:</b>\n\n"
        "/start - Welcome message and overview\n"
        "/help - Show this help message\n\n"
        "🎯 <b>How to use me:</b>\n\n"
        "📸 <b>Image Recognition:</b>\n"
        "   Just send me any photo! I'll identify what's in it\n"
        "   and show you the top 3 most likely objects with confidence scores.\n\n"
        "💬 <b>Short Messages:</b>\n"
        "   I'll show you message statistics (word count, character count)\n"
        "   and helpful tips.\n\n"
        "📝 <b>Long Messages (>200 characters):</b>\n"
        "   I'll automatically analyze your text and provide:\n"
        "   • 📊 Concise summary\n"
        "   • ✅ Extracted tasks/to-dos\n"
        "   • 😊 Sentiment analysis (positive/neutral/negative)\n\n"
        "💡 <b>Pro Tip:</b> The longer and more detailed your message,\n"
        "the better the AI analysis will be!",
        parse_mode="HTML",
    )


