from django.shortcuts import get_object_or_404
from django.utils.html import strip_tags
from django_socketio import events
from time import sleep

@events.on_message
def connect(request,socket,context,message):
    print "Timepass"
    while True:
        socket.send({"msg":"hi"})
