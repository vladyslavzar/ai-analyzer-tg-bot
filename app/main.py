"""FastAPI application with Telegram webhook endpoint."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Response, status
from fastapi.responses import JSONResponse

from app.bot import create_bot_application
from app.config import settings
from app.handlers.text import handle_text_message
from app.handlers.image import handle_image_message
from app.utils.events import log_event

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Global bot application
bot_application = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI app."""
    global bot_application

    # Startup: Initialize bot
    logger.info("Starting Telegram bot application...")
    bot_application = create_bot_application()
    await bot_application.initialize()
    await bot_application.start()

    # Set webhook if URL is configured
    if settings.telegram_webhook_url:
        webhook_url = f"{settings.telegram_webhook_url}/webhook"
        secret_token = settings.telegram_secret_token or None
        await bot_application.bot.set_webhook(
            url=webhook_url,
            secret_token=secret_token,
        )
        logger.info(f"Webhook set to: {webhook_url}")
    else:
        logger.warning("TELEGRAM_WEBHOOK_URL not set, webhook not configured")

    yield

    # Shutdown: Cleanup
    logger.info("Shutting down Telegram bot application...")
    if bot_application:
        await bot_application.stop()
        await bot_application.bot.delete_webhook()
        await bot_application.shutdown()


# Create FastAPI app
app = FastAPI(
    title="Telegram Bot API",
    description="Telegram bot with AI features and webhook support",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"status": "ok", "message": "Telegram Bot API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/webhook")
async def webhook(request: Request):
    """
    Telegram webhook endpoint.

    Receives updates from Telegram and processes them.
    """
    if not bot_application:
        return JSONResponse(
            {"error": "Bot application not initialized"},
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    # Verify secret token if configured
    if settings.telegram_secret_token:
        secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
        if secret_token != settings.telegram_secret_token:
            logger.warning("Invalid secret token in webhook request")
            return JSONResponse(
                {"error": "Invalid secret token"},
                status_code=status.HTTP_403_FORBIDDEN,
            )

    try:
        # Parse update from request
        update_data = await request.json()
        from telegram import Update

        update = Update.de_json(update_data, bot_application.bot)

        if update is None:
            logger.warning("Failed to parse update from webhook")
            return {"status": "error", "message": "Invalid update"}

        # Process update
        # For webhook mode, process_update handles the update directly
        await bot_application.process_update(update)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return JSONResponse(
            {"error": "Internal server error"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@app.post("/events/log")
async def log_event_endpoint(request: Request):
    """
    n8n event logging endpoint.

    Receives events from the bot and can be connected to n8n workflows.
    """
    try:
        event_data = await request.json()
        logger.info(f"Received event: {event_data.get('event_type', 'unknown')}")

        # Here you could process the event, store it, etc.
        # For now, we just acknowledge receipt

        return {
            "status": "ok",
            "message": "Event logged successfully",
            "event_type": event_data.get("event_type"),
        }

    except Exception as e:
        logger.error(f"Error logging event: {e}", exc_info=True)
        return JSONResponse(
            {"error": "Invalid request"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )

