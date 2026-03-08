from django.shortcuts import render
from .models import Message

def chat_room(request):
    # fetch all messages ordered by time
    messages = Message.objects.order_by("timestamp")
    # render chat room template with messages
    return render(request, "teacher_dashboard.html", {"messages": messages})

