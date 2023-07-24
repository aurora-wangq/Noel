import json

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

    def image(img):
        return MessageSegment('image', img)
        
class Message(list[MessageSegment]):
    def __init__(self, s):
        if isinstance(s, list) or isinstance(s, Message):
            super().__init__(s)
        elif isinstance(s, MessageSegment):
            super().__init__([ s ])
        elif isinstance(s, str):
            super().__init__([ MessageSegment.text(s) ])
        else:
            raise NotImplementedError("Unknown type")

    def __str__(self):
        return json.dumps([ x for x in self])
    
    def encode(self, encoding = 'utf-8', errors = 'strict'):
        return str(self).encode(encoding, errors)
    
class Event(dict):
    def __init__(self, msg, sender = '', avatar = '', title = '' ,title_level = ''):
        self['message'] = Message(msg)
        self['sender'] = sender
        self['avatar'] = avatar
        self['title'] = title
        self['title_level'] = title_level
    
    def __str__(self) -> str:
        return json.dumps(self)