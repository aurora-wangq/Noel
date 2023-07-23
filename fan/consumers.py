from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json
from .message import *
from PIL import Image
from io import BytesIO
import time

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
            f"NChat 0.0.2@Group {group}"), '')
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        data = json.loads(message['text'])
        
        for i in data['message']:
            if i['type'] == 'image':
                b64_str = i['data'].split(',')[1]
                b64 = base64.b64decode(b64_str)
                imagefile = Image.open(BytesIO(b64))
                timestamp = str(time.time())
                image_path = f'./media/chat_images/{timestamp}.jpg'
                imagefile.save(image_path)
                im = Image.open(image_path)
                (x, y) = im.size
                x1 = 160
                y1 = int(y * x1 / x)
                out = im.resize((x1, y1), Image.ANTIALIAS)
                out.save(image_path)
                with open(image_path, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read())
                    str_encode = str(encoded_string)
                    str_encode = str_encode.replace('\'','')
                    head = "data:image/jpeg;base64,"
                    i['data'] =head + str_encode[1:]

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
        self.send_msg(event['message']['message'], event['message']['sender'])

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("id")
        async_to_sync(self.channel_layer.group_discard)(
            group, self.channel_name)
        raise StopConsumer()
