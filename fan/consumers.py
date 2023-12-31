from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .message import *
from PIL import Image
from io import BytesIO
import base64
import collections

MAX_HISTORY_LENGTH = 100

chat_history = collections.deque(maxlen=MAX_HISTORY_LENGTH)

class ChatConsumer(WebsocketConsumer):
    def send_event(self, event: Event):
        self.send(str(event))

    def broadcast(self, group: int, event: Event):
        if not isinstance(event, dict):
            raise NotImplementedError()
        chat_history.append(event)
        async_to_sync(self.channel_layer.group_send)(group, {"type": "SendMessage", "message": event})

    def websocket_connect(self, message):
        self.accept()
        group = self.scope['url_route']['kwargs'].get("id")
        self.send_event(Event.notice(f"Connected to NChat rc-1 @Group {group}"))
        self.send_event(Event.info('history.begin'))
        for i in chat_history:
            self.send_event(i)
        self.send_event(Event.info('history.end'))
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        data = json.loads(message['text'])
        group = self.scope['url_route']['kwargs'].get("id")
        
        if data['type'] == 'init':
            self.broadcast(group, Event.notice(f"@{data['data']['sender']['username']} 进入聊天室"))
        elif data['type'] == 'message':
            for i in data['data']['message']:
                if i['type'] == 'image' and i['data'].startswith('data:image/'):
                    src = Image.open(BytesIO(base64.b64decode(i['data'].split(',')[1])))
                    res = BytesIO()
                    (x, y) = src.size
                    if x > 160:
                        src.resize((160, int(y * 160 / x)), Image.ANTIALIAS).save(res, src.format)
                    else:
                        src.save(res, src.format)
                    base = base64.b64encode(res.getvalue()).decode('ascii')
                    i['data'] = f"data:image/{src.format};base64," + base
            self.broadcast(group, Event(**data))

    def SendMessage(self, event):
        if isinstance(event['message'], Event):
            self.send_event(event['message'])
        elif isinstance(event['message'], dict):
            e = Event(event['message'])
            self.send_event(e)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("id")
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer()
