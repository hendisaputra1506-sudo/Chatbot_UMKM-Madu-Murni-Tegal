from flask import Flask, request, jsonify
from core import get_bot_reply

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "")
    reply = get_bot_reply(message)
    return jsonify({"reply": reply})

@app.route("/")
def home():
    return "Chatbot Madu Murni Tegal aktif"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
