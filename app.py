import os
import threading
from flask import Flask, request, jsonify
from telegram import Update, Bot
from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    Filters,
    CallbackContext
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
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Halo Kak 👋\nSaya asisten *Madu Murni Tegal* 🍯\nSilakan tanya seputar produk ya 😊",
        parse_mode="Markdown"
    )

def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    reply = get_bot_reply(user_message)
    update.message.reply_text(reply, parse_mode="Markdown")


# ===============================
# RUN TELEGRAM BOT (THREAD)
# ===============================
def run_telegram_bot():
    updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    print("🤖 Telegram Bot berjalan...")
    updater.start_polling()
    updater.idle()


# ===============================
# ENTRY POINT
# ===============================
if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
