from core import get_bot_reply
import json

def handler(request):
    if request.method != "POST":
        return {
            "statusCode": 405,
            "body": json.dumps({"reply": "Method not allowed"})
        }

    data = request.json()
    msg = data.get("message", "")

    reply = get_bot_reply(msg)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": reply})
    }
