import asyncio
from telegram import Update
from telegram.ext import Application

app = Application.builder().token("YOUR_BOT_TOKEN").build()

async def main():
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())  # Yeh ensure karega ki event loop sahi se handle ho
