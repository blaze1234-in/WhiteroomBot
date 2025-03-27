from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import asyncio

# Telegram Bot Token (BotFather se lo)
TOKEN = "tumhara_bot_token"

# Start Command
async def start(update: Update, context):
    await update.message.reply_text("Whiteroom Bot is Online!")

# Main Function
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("Whiteroom Bot is running...")
    await app.run_polling()

# Run Bot
if __name__ == "__main__":
    asyncio.run(main())

