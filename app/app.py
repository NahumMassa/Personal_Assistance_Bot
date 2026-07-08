# pyrefly: ignore [missing-import]
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from os import getenv
from app.handlers.handlers import register_transaction_telegram
from app.handlers.handlers import register_category_telegram


load_dotenv()

TELEGRAM_BOT_TOKEN = getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN is not set")

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello World!")




print("Bot is running...")
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("hello", say_hello))
app.add_handler(CommandHandler("transaction", register_transaction_telegram))
app.add_handler(CommandHandler("add_category", register_category_telegram))

app.run_polling(allowed_updates=Update.ALL_TYPES)