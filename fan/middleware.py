from django.http import HttpRequest
from django.http.response import HttpResponseServerError
from django.shortcuts import render, redirect
import random

probability = 0.2

# Hard-coded blacklist middleware
class BlacklistMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.blacklist = [
            {
                "uid": 2,
                "banned_from": [
                    '/fissure_traveler',
                    '/chat'
                ]
            }
        ]

    def __call__(self, request: HttpRequest):
        id = request.user.id
        a = list(filter(lambda x: x['uid'] == id, self.blacklist))
        if not a:
            return self.get_response(request)
        else:
            if any(request.path.startswith(x) for x in a[0]['banned_from']):
                return render(request, "fan/error.html", {
                    'hit': random.random() < probability
                })
            else:
                return self.get_response(request)
