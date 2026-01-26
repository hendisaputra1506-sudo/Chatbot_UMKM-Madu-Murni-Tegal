import json
from core import get_bot_reply

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"reply": "Method not allowed"})
        }

    data = request.json()
    message = data.get("message", "")

    reply = get_bot_reply(message)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": reply})
    }
