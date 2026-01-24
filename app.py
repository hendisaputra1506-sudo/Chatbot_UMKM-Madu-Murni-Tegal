import os
import asyncio
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
    filters
)

from core import get_bot_reply

# ===============================
# KONFIGURASI
# ===============================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN belum di-set di Railway Variables")

# ===============================
# FLASK APP
# ===============================
app = Flask(__name__)

@app.route("/")
def home():
    return "Chatbot Madu Murni Tegal aktif"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    message = data.get("message", "")
    reply = get_bot_reply(message)
    return jsonify({"reply": reply})


# ===============================
# TELEGRAM HANDLERS
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo Kak 👋\nSaya asisten *Madu Murni Tegal* 🍯\nSilakan tanya seputar produk ya 😊",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = get_bot_reply(user_message)
    await update.message.reply_text(reply, parse_mode="Markdown")


# ===============================
# RUN TELEGRAM BOT (ASYNC)
# ===============================
async def run_telegram_bot():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Telegram Bot berjalan...")
    await application.run_polling()


# ===============================
# ENTRY POINT
# ===============================
import threading

def start_telegram():
    asyncio.run(run_telegram_bot())

if __name__ == "__main__":
    threading.Thread(target=start_telegram, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

