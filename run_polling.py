#!/usr/bin/env python3.12
"""Run bot in polling mode for local testing.

This script runs the bot in polling mode, which is ideal for local development.
It doesn't require a webhook URL or exposing your local server.
"""

import asyncio
import logging
import signal
import sys

from app.bot import create_bot_application
from app.config import settings

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_event = asyncio.Event()


def signal_handler(sig, frame):
    """Handle shutdown signals."""
    logger.info("Shutdown signal received...")
    shutdown_event.set()


async def main():
    """Run bot in polling mode."""
    logger.info("=" * 60)
    logger.info("Starting Telegram Bot in POLLING mode")
    logger.info("=" * 60)
    logger.info(f"Bot token: {settings.telegram_bot_token[:10]}..." if settings.telegram_bot_token else "NOT SET")
    logger.info("Press Ctrl+C to stop the bot")
    logger.info("=" * 60)

    if not settings.telegram_bot_token:
        logger.error("ERROR: TELEGRAM_BOT_TOKEN is not set in .env file!")
        logger.error("Please create a .env file with your bot token.")
        sys.exit(1)

    application = create_bot_application()

    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        # Start the bot
        async with application:
            await application.start()
            await application.updater.start_polling(
                allowed_updates=["message", "callback_query"],
                drop_pending_updates=True,  # Clear any pending updates on start
            )
            logger.info("✅ Bot is running and polling for updates...")
            logger.info("   Send a message to your bot on Telegram to test it!")

            # Wait for shutdown signal
            await shutdown_event.wait()

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received...")
    except Exception as e:
        logger.error(f"Error running bot: {e}", exc_info=True)
    finally:
        logger.info("Stopping bot...")
        try:
            if application.updater.running:
                await application.updater.stop()
            await application.stop()
            await application.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
        logger.info("Bot stopped. Goodbye!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Shutdown complete.")


