import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler

async def start(update: Update, context):
    await update.message.reply_text("Hello! I'm WhiteroomBot.")

def main():
    app = Application.builder().token("7932045647:AAFaZhRxrbagNuwXDrzY_FUhu1VFWv9nFrc").build()
    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")

    try:
        app.run_polling()
    except RuntimeError as e:
        if "Cannot close a running event loop" in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(app.stop())

if __name__ == "__main__":
    main()
