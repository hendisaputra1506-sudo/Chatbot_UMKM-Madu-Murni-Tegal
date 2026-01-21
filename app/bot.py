import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
    CommandHandler
)

from core import get_bot_reply

# ===============================
# LOAD ENV
# ===============================
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN belum di-set di .env")

# ===============================
# COMMAND /START
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = get_bot_reply("halo")
    await update.message.reply_text(welcome_text)

# ===============================
# HANDLE CHAT
# ===============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    bot_response = get_bot_reply(user_message)
    await update.message.reply_text(bot_response)

# ===============================
# MAIN
# ===============================
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    print("🤖 Bot Telegram Madu Murni Tegal berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
