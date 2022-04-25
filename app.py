from cProfile import run
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('UVHgsMIfRWsSsCYODyl3nFwAYXo6h39v1Qt/Kwm9ewVJ2zc1sTGBTtxYq2e3eAbQWYl8BGWIRZDegWZYbwrcl4e09R4cUcxtpHufjvwed0VdukUcZefs0JZJwuDHSai2jhMZs9L4gFGBRFkjl+E6VgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('dbc0b0f87536a6169c3eeb7ec0f9be7b')

@app.route("/")
def test():
    return "OK"

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

from time import time
users = {}
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    if event.message.text == "開始":
        reply_message = "計測開始"
        if not userId in users:
            users[userId] = {}
            users[userId]["total"] = 0
        users[userId] ["start"] = time()
    else:
        end = time()
        difference = int(end - users[userId]["start"])
        users[userId]["total"] += difference
        hour = difference // 3600
        minute = (difference % 3600) // 60
        second = difference % 60
        reply_message = f"今の時間は{hour}時間{minute}分{second}秒だよ。合計で{users[userId]['total']}秒だよ。お疲れ様！"    
    
    
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message))


if __name__ == "__main__":
    app.run()