from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate, MessageAction, QuickReply, QuickReplyButton, CarouselTemplate, CarouselColumn

app = FastAPI()


LINE_CHANNEL_ACCESS_TOKEN = 'your_access_token'
LINE_CHANNEL_SECRET = 'secret'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.post("/linepost")
async def callback(request: Request):
    
    signature = request.headers.get('X-Line-Signature')
    body = await request.body()
    try:
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text == "hello":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello, welcome to Cinemalism!')
        )
    elif text == "button":
        buttons_template = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                title='Menu',
                text='Please select',
                actions=[
                    MessageAction(label='Option 1', text='You selected option 1'),
                    MessageAction(label='Option 2', text='You selected option 2')
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)
    elif text == "quick reply":
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="Option A", text="A")),
            QuickReplyButton(action=MessageAction(label="Option B", text="B"))
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Choose an option", quick_reply=quick_reply)
        )
    elif text == "carousel":
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
                title="Option 1",
                text="Description for option 1",
                actions=[
                    MessageAction(label="Select Option 1", text="You selected option 1")
                ]
            ),
            CarouselColumn(
                title="Option 2",
                text="Description for option 2",
                actions=[
                    MessageAction(label="Select Option 2", text="You selected option 2")
                ]
            ),
            CarouselColumn(
                title="Option 3",
                text="Description for option 3",
                actions=[
                    MessageAction(label="Select Option 3", text="You selected option 3")
                ]
            )
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)
    
@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)


