from flask import Flask, request
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext, MemoryStorage, ConversationState
from botbuilder.schema import Activity

app = Flask(__name__)

# Azure Bot Credentials
APP_ID = "7aa1fb2e-237c-4efd-958e-6d08f1aa5e1a"
APP_PASSWORD = "Que8Q~AoDQpou.t~eipnc2YkD11kZJDISAe1ratp"

settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(settings)

async def on_message_activity(turn_context: TurnContext):
    user_message = turn_context.activity.text
    # Here you can call OpenAI GPT to generate a reply
    await turn_context.send_activity(f"Echo: {user_message}")

@app.route("/api/messages", methods=["POST"])
def messages():
    if "application/json" in request.headers["Content-Type"]:
        body = request.json
    else:
        return "Unsupported Media Type", 415

    activity = Activity().deserialize(body)
    auth_header = request.headers.get("Authorization", "")

    async def aux_func(turn_context):
        await on_message_activity(turn_context)

    task = adapter.process_activity(activity, auth_header, aux_func)
    return "", 202

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3978)
