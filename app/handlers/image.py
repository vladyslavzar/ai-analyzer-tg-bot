"""Image message handler."""

from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from app.utils.classify import classify_image
from app.utils.events import log_event
from app.utils.image_descriptions import get_image_description, get_category_description


async def handle_image_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handle incoming image messages.

    Downloads the image, classifies it, and returns the prediction.
    """
    if not update.message or not update.message.photo:
        return

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    # Get the largest photo
    photo = update.message.photo[-1]

    # Send processing message
    processing_msg = await update.message.reply_text("🔍 Analyzing image...")

    try:
        # Download image
        file = await context.bot.get_file(photo.file_id)
        image_bytes = await file.download_as_bytearray()

        # Classify image - get top 3 predictions
        predictions = classify_image(bytes(image_bytes), top_k=3)

        # Format response using HTML (more reliable than Markdown)
        from telegram.helpers import escape
        
        # Get main description
        top_label, top_confidence = predictions[0]
        main_description = get_image_description(top_label, top_confidence)
        category_desc = get_category_description(top_label)
        
        response_parts = [
            "🖼️ <b>Image Recognition Analysis</b>\n",
            f"📸 {category_desc.lower()}.\n",
            f"🎯 <b>Primary Identification:</b>\n{main_description}\n",
            "\n📊 <b>Detailed Predictions:</b>\n"
        ]
        
        for i, (label, confidence) in enumerate(predictions, 1):
            confidence_percent = confidence * 100
            escaped_label = escape(label.replace("_", " ").title())
            description = get_image_description(label, confidence)
            
            # Add emoji for ranking
            emoji = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            
            # Confidence level
            if confidence_percent > 80:
                conf_level = "Very High"
            elif confidence_percent > 50:
                conf_level = "High"
            elif confidence_percent > 30:
                conf_level = "Medium"
            else:
                conf_level = "Low"
            
            response_parts.append(
                f"{emoji} <b>{i}.</b> {escaped_label}\n"
                f"   {description}\n"
                f"   Confidence: {confidence_percent:.1f}% ({conf_level})\n"
            )
        
        response_text = "\n".join(response_parts)

        await processing_msg.edit_text(response_text, parse_mode="HTML")

        # Log event to n8n
        await log_event(
            "image_message",
            {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "chat_id": chat_id,
                "file_id": photo.file_id,
                "predictions": [
                    {"label": label, "confidence": conf * 100} 
                    for label, conf in predictions
                ],
            },
        )

    except Exception as e:
        error_msg = f"❌ Error processing image: {str(e)}"
        await processing_msg.edit_text(error_msg)

        # Log error event
        await log_event(
            "image_message",
            {
                "timestamp": datetime.utcnow().isoformat(),
                "user_id": user_id,
                "chat_id": chat_id,
                "error": str(e),
            },
        )


