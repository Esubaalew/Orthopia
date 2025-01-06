from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
)
import os
import logging
from telegram import Update
from .models import Reaction, Comment  # Ensure to import your models

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command for Orthopia Bot"""
    await update.message.reply_text(
        "Welcome to Orthopia! 🌟\n\nOrthopia is a platform combining the cultural and spiritual essence of Orthodox Tewahedo and Ethiopian traditions. "
        "Feel free to explore features, share posts, and engage with the community."
    )

async def react(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """React to a post."""
    if len(context.args) != 2:
        await update.message.reply_text("Usage: /react <post_id> <reaction_type>")
        return

    post_id, reaction_type = context.args
    user = update.message.from_user

    valid_reactions = ['like', 'dislike', 'love', 'laugh', 'sad', 'angry']
    if reaction_type not in valid_reactions:
        await update.message.reply_text("Invalid reaction type. Choose from: " + ", ".join(valid_reactions))
        return

    reaction, created = Reaction.objects.get_or_create(
        user=user.id,
        post_id=post_id,
        type=reaction_type
    )

    if created:
        await update.message.reply_text(f"Reacted with {reaction_type} to post {post_id}.")
    else:
        await update.message.reply_text("You have already reacted to this post.")

async def comment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Comment on a post."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /comment <post_id> <comment_text>")
        return

    post_id = context.args[0]
    comment_text = ' '.join(context.args[1:])
    user = update.message.from_user

    Comment.objects.create(
        post_id=post_id,
        user=user.id,
        content=comment_text
    )

    await update.message.reply_text(f"Commented on post {post_id}: {comment_text}")

async def view_comments(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """View comments on a post."""
    if len(context.args) != 1:
        await update.message.reply_text("Usage: /view_comments <post_id>")
        return

    post_id = context.args[0]
    comments = Comment.objects.filter(post_id=post_id)

    if comments.exists():
        comment_texts = "\n".join([f"{comment.user.username}: {comment.content}" for comment in comments])
        await update.message.reply_text(f"Comments for post {post_id}:\n{comment_texts}")
    else:
        await update.message.reply_text("No comments for this post.")

async def bot_tele(text):
    """Initialize the bot and set up handlers."""
    application = (
        Application.builder().token(os.getenv('TOKEN')).build()
    )

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("react", react))
    application.add_handler(CommandHandler("comment", comment))
    application.add_handler(CommandHandler("view_comments", view_comments))

    # Start application
    await application.bot.set_webhook(url=os.getenv('webhook'))
    await application.update_queue.put(
        Update.de_json(data=text, bot=application.bot)
    )
    async with application:
        await application.start()
        await application.stop()