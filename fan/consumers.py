from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .message import *
from PIL import Image
from io import BytesIO
import time

chat_history = []

class ChatConsumer(WebsocketConsumer):
    def send_msg(self, msg, sender):
        if isinstance(msg, MessageSegment):
            msg = Message([msg])
        elif isinstance(msg, str):
            msg = Message([MessageSegment.text(msg)])
        self.send(str(Event(msg, sender)))

    def websocket_connect(self, message):
        self.accept()
        group = self.scope['url_route']['kwargs'].get("id")
        self.send_msg(MessageSegment.notice(f"Connected to NChat pre-alpha-2@Group {group}"), '')
        for i in chat_history:
            self.send_msg(i['message'], i['sender'])
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        data = json.loads(message['text'])
        
        for i in data['message']:
            if i['type'] == 'image' and i['data'].startswith('data:image/'):
                src = Image.open(BytesIO(base64.b64decode(i['data'].split(',')[1])))
                res = BytesIO()
                (x, y) = src.size
                src.resize((160, int(y * 160 / x)), Image.ANTIALIAS).save(res, 'JPEG')
                base = base64.b64encode(res.getvalue()).decode('ascii')
                i['data'] = "data:image/jpeg;base64," + base

        group = self.scope['url_route']['kwargs'].get("id")
        if data.get('init'):
            async_to_sync(self.channel_layer.group_send)(group, {"type": "SendMessage", "message": {
                "sender": "",
                "message": [
                    {
                        "type": "notice",
                        "data": f"{data['sender']} 进入聊天室"
                    }
                ]
            }})
        else:
            async_to_sync(self.channel_layer.group_send)(group, {"type": "SendMessage", "message": data})
        #print("Received:", data['message'])

    def SendMessage(self, event):
        chat_history.append(event['message'])
        self.send_msg(event['message']['message'], event['message']['sender'])

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("id")
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()
