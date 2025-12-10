"""Text message handler."""

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from app.config import settings
from app.utils.events import log_event
from app.utils.llm import analyze_text

# Threshold for considering a message "long" (characters)
LONG_TEXT_THRESHOLD = 200


async def handle_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming text messages.

    For long messages (>200 chars), performs AI analysis.
    For short messages, responds with echo.
    """
    if not update.message or not update.message.text:
        return

    text = update.message.text
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Log event to n8n
    await log_event(
        "text_message",
        {
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "chat_id": chat_id,
            "message_text": text,
            "message_length": len(text),
        },
    )

    # Check if message is long enough for AI analysis
    if len(text) > LONG_TEXT_THRESHOLD:
        # Send processing message
        processing_msg = await update.message.reply_text(
            "🤖 Analyzing your message with AI..."
        )

        # Perform AI analysis
        analysis = await analyze_text(text)

        # Check if LLM API key is configured
        if not settings.llm_api_key:
            # Provide helpful message if API key is not set
            response_text = (
                "📊 **AI Analysis**\n\n"
                "⚠️ **LLM API key not configured**\n\n"
                "To enable AI analysis, add your `LLM_API_KEY` to the `.env` file.\n"
                "You can get a free API key from https://openrouter.ai\n\n"
                f"📝 **Message length:** {len(text)} characters\n"
                f"💡 **Tip:** Messages longer than {LONG_TEXT_THRESHOLD} characters "
                "will be analyzed when LLM_API_KEY is configured."
            )
        else:
            # Format response with analysis
            response_parts = [
                "📊 **AI Analysis**",
                "",
                f"📝 **Summary:**\n{analysis['summary']}",
                "",
            ]

            if analysis["tasks"]:
                tasks_text = "\n".join(f"• {task}" for task in analysis["tasks"])
                response_parts.append(f"✅ **Tasks/To-dos:**\n{tasks_text}\n")

            sentiment_emoji = {
                "positive": "😊",
                "negative": "😟",
                "neutral": "😐",
            }.get(analysis["sentiment"], "😐")

            response_parts.append(
                f"{sentiment_emoji} **Sentiment:** {analysis['sentiment'].title()}"
            )

            response_text = "\n".join(response_parts)

        # Update message with results
        await processing_msg.edit_text(response_text, parse_mode="Markdown")

        # Log LLM analysis event
        await log_event(
            "llm_analysis",
            {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "chat_id": chat_id,
                "original_text": text,
                "analysis": analysis,
            },
        )
    else:
        # Provide useful information for short messages
        word_count = len(text.split())
        char_count = len(text)
        
        # Add some helpful responses based on content
        response_parts = []
        
        # Check for questions
        if text.strip().endswith("?"):
            response_parts.append("❓ I see you asked a question!")
            response_parts.append("💡 Try asking me in a longer message for a detailed AI analysis.")
        
        # Check for common greetings
        greetings = ["hello", "hi", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        if any(text.lower().startswith(g) for g in greetings):
            response_parts.append("👋 Hello! Nice to meet you!")
            response_parts.append("📸 Send me a photo to identify what's in it!")
            response_parts.append(f"📝 Or send a longer message (>200 chars) for AI analysis!")
        else:
            response_parts.append(f"📊 <b>Message Stats:</b>")
            response_parts.append(f"• Words: {word_count}")
            response_parts.append(f"• Characters: {char_count}")
            response_parts.append("")
            response_parts.append(f"💡 <b>Tip:</b> Send a message longer than {LONG_TEXT_THRESHOLD} characters for AI-powered analysis:")
            response_parts.append("   • Summary generation")
            response_parts.append("   • Task extraction")
            response_parts.append("   • Sentiment analysis")
        
        response_text = "\n".join(response_parts)
        await update.message.reply_text(response_text, parse_mode="HTML")


