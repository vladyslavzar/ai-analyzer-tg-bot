"""Event logging utilities for n8n integration."""

import json
from typing import Any

import httpx

from app.config import settings


async def log_event(event_type: str, data: dict[str, Any]) -> bool:
    """
    Send event to n8n webhook endpoint.

    Args:
        event_type: Type of event (text_message, image_message, llm_analysis)
        data: Event data payload

    Returns:
        True if successful, False otherwise
    """
    if not settings.n8n_webhook_url:
        # Silently fail if n8n webhook is not configured
        return False

    payload = {
        "event_type": event_type,
        "timestamp": data.get("timestamp"),
        "user_id": data.get("user_id"),
        "chat_id": data.get("chat_id"),
        "data": data,
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                settings.n8n_webhook_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return True
    except Exception:
        # Log error but don't fail the bot operation
        return False


