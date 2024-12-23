from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
import os
import logging
from telegram import Update
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command for Orthopia Bot"""
    await update.message.reply_text(
        "Welcome to Orthopia! 🌟\n\nOrthopia is a platform combining the cultural and spiritual essence of Orthodox Tewahedo and Ethiopian traditions. "
        "Feel free to explore features, share posts, and engage with the community."
    )


async def bot_tele(text):
    # Create application
    application = (
        Application.builder().token(os.getenv('TOKEN')).build()
    )

    
    # Register handlers
    application.add_handler(CommandHandler("start", start))

    # Start application
    await application.bot.set_webhook(url=os.getenv('webhook'))
    await application.update_queue.put(
        Update.de_json(data=text, bot=application.bot)
    )
    async with application:
        await application.start()
        await application.stop()
