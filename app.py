import os
import threading
from flask import Flask, request, jsonify
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler

from core import get_bot_reply

# ===============================
# KONFIGURASI
# ===============================
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN belum di-set di Railway Variables")

# ===============================
# FLASK APP (WEB API)
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
# TELEGRAM BOT
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo Kak 👋\nSaya asisten Madu Murni Tegal.\nSilakan tanya seputar madu ya 😊"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = get_bot_reply(user_message)
    await update.message.reply_text(reply)

def run_telegram_bot():
    app_telegram = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app_telegram.add_handler(CommandHandler("start", start))
    app_telegram.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Telegram Bot berjalan...")
    app_telegram.run_polling()


# ===============================
# JALANKAN KEDUANYA
# ===============================
if __name__ == "__main__":
    threading.Thread(target=run_telegram_bot).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
