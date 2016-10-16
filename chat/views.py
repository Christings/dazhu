from django.shortcuts import render
from models import Message
# Create your views here.
def chat_room(request):
    # If the room with the given label doesn't exist, automatically create it
    # upon first visit (a la etherpad).
    # We want to show the last 50 messages, ordered most-recent-last
    messages = reversed(Message.objects.order_by('-timestamp')[:50])

    return render(request, "chat/room.html", {
        'messages': messages,
    })