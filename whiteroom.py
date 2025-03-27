import logging
import asyncio
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, filters, CallbackContext
import os

# Logging setup
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Bot Token & Admin IDs (from Railway Environment Variables)
BOT_TOKEN = os.getenv("BOT_TOKEN")
import os

ADMIN_IDS = os.getenv("ADMIN_IDS", "").strip()

if ADMIN_IDS:  
    ADMIN_IDS = list(map(int, ADMIN_IDS.split(",")))  
else:  
    ADMIN_IDS = []  # Agar empty ho toh empty list bana do

print("Loaded Admin IDs:", ADMIN_IDS)  # Debugging ke liye (baad me hata sakte ho)


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

# Start bot
async def main():
    await app.run_polling()

import asyncio

async def main():
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Properly start the bot
    except RuntimeError as e:
        print(f"Error: {e}")
