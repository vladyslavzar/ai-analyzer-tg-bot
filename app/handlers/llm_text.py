"""LLM-specific text handler (for explicit AI analysis requests)."""

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from app.utils.events import log_event
from app.utils.llm import analyze_text


async def handle_llm_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle explicit LLM analysis requests (e.g., /analyze command).

    This handler can be used for commands that explicitly request AI analysis.
    """
    if not update.message or not update.message.text:
        return

    # Extract text (remove command if present)
    text = update.message.text
    if text.startswith("/"):
        # If it's a command, get the argument
        parts = text.split(" ", 1)
        if len(parts) > 1:
            text = parts[1]
        else:
            await update.message.reply_text(
                "Please provide text to analyze. Usage: /analyze <your text>"
            )
            return

    if not text.strip():
        await update.message.reply_text("Please provide text to analyze.")
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Send processing message
    processing_msg = await update.message.reply_text("🤖 Analyzing with AI...")

    # Perform AI analysis
    analysis = await analyze_text(text)

    # Format response
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


