from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
import json

class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        print("正在连接...")
        self.accept()
        print("连接成功！")
        group = self.scope['url_route']['kwargs'].get("id")
        self.send(f"[系统消息]版本号：NChat.0.0.1\n[系统消息]群组号：{group}")
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        data = json.loads(message['text'])
        if data['text'] == '':
            self.send("[系统消息]当前用户：" + data['nickname'] + " @" + data['username'])
        else:
            group = self.scope['url_route']['kwargs'].get("id")
            #self.send(data['text'])
            async_to_sync(self.channel_layer.group_send)(group, {"type": "SendMessage", "message": data})
            print("接收并广播：",data['text'])

    def SendMessage(self, event):
        text = event['message']['text']
        self.send(event['message']['nickname'] + '：' + text)

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get("id")
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        print("连接丢失\用户退出！")
        raise StopConsumer()
    #<fan.consumers.ChatConsumer object at 0x0000015EF6652CD0>