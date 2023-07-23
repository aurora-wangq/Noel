from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .message import *


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
        self.send_msg(MessageSegment.notice(
            f"NChat 0.0.1@Group {group}"), '')
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        data = json.loads(message['text'])
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
        print("Received:", data['message'])

    def SendMessage(self, event):
        self.send_msg(event['message']['message'], event['message']['sender'])

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("id")
        async_to_sync(self.channel_layer.group_discard)(
            group, self.channel_name)
        raise StopConsumer()
