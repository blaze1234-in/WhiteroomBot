import logging
import asyncio
import os
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, filters, CallbackContext

# Logging setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Bot Token & Admin IDs (from Railway Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_IDS = os.getenv("ADMIN_IDS", "").strip()
ADMIN_IDS = list(map(int, ADMIN_IDS.split(","))) if ADMIN_IDS else []

print("Loaded Admin IDs:", ADMIN_IDS)  # Debugging ke liye

# Initialize bot
app = Application.builder().token(BOT_TOKEN).build()

# Warn storage
warns = {}

# Command to warn users
async def warn(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMIN_IDS:
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /warn @user reason")
        return

    user = update.message.reply_to_message.from_user
    reason = " ".join(context.args)
    
    warns[user.id] = warns.get(user.id, 0) + 1
    await update.message.reply_text(f"{user.first_name} has been warned! Reason: {reason} (Total Warns: {warns[user.id]})")

    if warns[user.id] >= 3:
        await update.effective_chat.ban_member(user.id)
        await update.message.reply_text(f"{user.first_name} has been banned for exceeding warn limit!")

# Command to mute users
async def mute(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMIN_IDS:
        return

    user = update.message.reply_to_message.from_user
    await update.effective_chat.restrict_member(user.id, ChatPermissions(can_send_messages=False))
    await update.message.reply_text(f"{user.first_name} has been muted!")

# Command to unmute users
async def unmute(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMIN_IDS:
        return

    user = update.message.reply_to_message.from_user
    await update.effective_chat.restrict_member(user.id, ChatPermissions(can_send_messages=True))
    await update.message.reply_text(f"{user.first_name} has been unmuted!")

# Command to ban users
async def ban(update: Update, context: CallbackContext):
    if update.message.from_user.id not in ADMIN_IDS:
        return

    user = update.message.reply_to_message.from_user
    await update.effective_chat.ban_member(user.id)
    await update.message.reply_text(f"{user.first_name} has been banned!")

# Add command handlers
app.add_handler(CommandHandler("warn", warn, filters.REPLY))
app.add_handler(CommandHandler("mute", mute, filters.REPLY))
app.add_handler(CommandHandler("unmute", unmute, filters.REPLY))
app.add_handler(CommandHandler("ban", ban, filters.REPLY))

# Start bot (Proper Railway Event Loop Handling)
async def main():
    print("Bot is running...")
    await app.run_polling()

# 🚀 Run without event loop issues!
if __name__ == "__main__":
    try:
        asyncio.run(main())  # Only use asyncio.run() directly (Safe method)
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.create_task(main())
        loop.run_forever()



