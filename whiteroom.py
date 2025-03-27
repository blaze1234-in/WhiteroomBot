import asyncio
import sys
from telegram.ext import Application

app = Application.builder().token("YOUR_BOT_TOKEN").build()

async def main():
    await app.run_polling()

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # Windows ke liye fix
    asyncio.run(main())  # Proper event loop handling
