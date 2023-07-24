from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .message import *
from PIL import Image
from io import BytesIO
import base64

chat_history = []

class ChatConsumer(WebsocketConsumer):
    def send_event(self, event: Event):
        self.send(str(event))

    def broadcast(self, group: int, event: Event):
        if isinstance(event, dict):
            event = Event(event['message'], event['sender'])
        chat_history.append(event)
        async_to_sync(self.channel_layer.group_send)(group, {"type": "SendMessage", "message": event})

    def websocket_connect(self, message):
        self.accept()
        group = self.scope['url_route']['kwargs'].get("id")
        self.send_event(Event(MessageSegment.notice(f"Connected to NChat rc-1 @Group {group}")))
        for i in chat_history:
            self.send_event(Event(i['message'], i['sender']))
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        data = json.loads(message['text'])
        
        for i in data['message']:
            if i['type'] == 'image' and i['data'].startswith('data:image/'):
                src = Image.open(BytesIO(base64.b64decode(i['data'].split(',')[1])))
                res = BytesIO()
                (x, y) = src.size
                src.resize((160, int(y * 160 / x)), Image.ANTIALIAS).save(res, src.format)
                base = base64.b64encode(res.getvalue()).decode('ascii')
                i['data'] = f"data:image/{src.format};base64," + base

        group = self.scope['url_route']['kwargs'].get("id")
        if data.get('init'):
            self.broadcast(group, Event(MessageSegment.notice(f"{data['sender']['nickname']} 进入聊天室")))
        else:
            self.broadcast(group, data)

    def SendMessage(self, event):
        if isinstance(event['message'], Event):
            self.send_event(event['message'])
        elif isinstance(event['message'], dict):
            e = Event(event['message']['message'], event['message']['sender'])
            self.send_event(e)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("id")
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()
