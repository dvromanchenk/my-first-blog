import json

from django.shortcuts import render, redirect
from django.shortcuts import render
from django.utils.safestring import mark_safe

from chat.models import Chat


def generate_room_name(room_name):
    new_room_name = room_name
    n = 0
    while True:
        try:
            Chat.objects.get(theme=new_room_name)
        except Chat.DoesNotExist:
            break
        else:
            n += 1
            new_room_name = f'{room_name}-{n}'

    return new_room_name


def index(request):
    return render(request, 'chat/index.html', {})


def room(request, room_name):
    # add open chat to db
    if not request.user.is_staff:
        room_name = generate_room_name(room_name)
        chat = Chat.objects.create(theme=room_name)
    else:
        chat = Chat.objects.get(theme=room_name)

    history = ''
    for message in chat.chatmessage_set.all():
        history += message.message + '\n'

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'chat': chat,
        'history': history
    })


def chat_list(request):
    theme = request.POST.get('chat_theme')
    if request.method == 'POST':
        room(request, theme)
    else:
        chat_list = Chat.objects.all()
        return render(request, 'chat/chat_list.html', {'chat_list': chat_list})


def disconnect(request, room_name):
    Chat.objects.get(theme=room_name).delete()
    return redirect('post_list')
