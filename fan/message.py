import json
import base64
import requests

class MessageSegment(dict):
    def __init__(self, type = '', data = {}):
        self['type'] = type
        self['data'] = data
    
    def __str__(self):
        return json.dumps(self)
    
    def text(s):
        return MessageSegment('text', s)
    
    def notice(s):
        return MessageSegment('notice', s)

    def image(img: str | bytes):
        if isinstance(img, str):
            return MessageSegment('image',{
                'subtype': 'url',
                'data': img
            })
        elif isinstance(img, bytes):
            base = base64.b64encode(img)
            return MessageSegment('image',{
                'subtype': 'base64',
                'data': base
            })
        
class Message(list[MessageSegment]):
    def __str__(self):
        return json.dumps([ x for x in self])
    
    def encode(self, encoding = 'utf-8', errors = 'strict'):
        return str(self).encode(encoding, errors)
    
class Event(dict):
    def __init__(self, msg, sender):
        self['message'] = msg
        self['sender'] = sender
    
    def __str__(self) -> str:
        return json.dumps(self)