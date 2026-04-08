from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.http import JsonResponse

from messenger.forms import SignUpForm, SignInForm, SendMessageForm, AddChatForm
from messenger.models import User, Chat, Message

from json import loads


def index(request):
    user = request.user

    if user.is_authenticated:
        chats = Chat.objects.filter(users=user).distinct()

        messages = Message.objects.filter(chat=user.current_chat)

        current_chat_id = None

        if user.current_chat:
            current_chat_id = user.current_chat.id

        context = {
            'send_message_form': SendMessageForm(current_chat_id=current_chat_id),
            'add_chat_form': AddChatForm,
            'chats': chats,
            'messages': messages
        }

        return render(request, 'index.html', context)

    return redirect('sign_in')


def sign_in(request):
    if request.method == 'POST':
        form = SignInForm(request=request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            login(request, user)

        else:
            context = {'form': form}

            return render(request, 'sign_in.html', context)

        return redirect('index')

    context = {'form': SignInForm}

    return render(request, 'sign_in.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            user = form.save()

            login(request, user)

        else:
            context = {'form': form}

            return render(request, 'sign_up.html', context)

        return redirect('index')

    context = {'form': SignUpForm}

    return render(request, 'sign_up.html', context)


def sign_out(request):
    logout(request)

    return redirect('index')


def create_new_chat(request):
    user = request.user

    if request.method == 'POST' and user.is_authenticated:
        form = AddChatForm(request.POST, user=user)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            other_user = User.objects.filter(username=username).first()

            if other_user is not None:
                new_chat = form.save(commit=False)

                new_chat.name = f'Чат {user.username} и {username}'

                new_chat.save()

                new_chat.users.add(user)
                new_chat.users.add(other_user)

        else:
            chats = Chat.objects.filter(users=user).distinct()

            messages = Message.objects.filter(chat=user.current_chat)

            context = {
                'send_message_form': SendMessageForm,
                'add_chat_form': form,
                'chats': chats,
                'messages': messages
            }

            return render(request, 'index.html', context)

    return redirect('index')


def get_chat_messages(request):
    if request.method == 'POST':
        user = request.user

        id = loads(request.body).get('id')

        chat = Chat.objects.filter(id=id).first()

        user.current_chat = chat

        user.save()

        if chat and user.is_authenticated:
            if user in chat.users.all():
                messages = list(Message.objects.filter(chat=chat).values('sender__username', 'text'))

                return JsonResponse(messages, safe=False)

        else:
            return JsonResponse({}, safe=False, status=404)

    return redirect('index')


def send_message(request):
    user = request.user

    if request.method == 'POST' and user.is_authenticated:
        form = SendMessageForm(loads(request.body), current_chat_id=user.current_chat.id)

        if form.is_valid():
            id = form.cleaned_data.get('chat_id')
            chat = Chat.objects.filter(id=id).first()

            new_message = form.save(commit=False)

            new_message.sender = user
            new_message.text = form.cleaned_data.get('message')
            new_message.chat = chat

            new_message.save()

            messages = list(Message.objects.filter(chat=user.current_chat).values('sender__username', 'text'))

            return JsonResponse(messages, safe=False)

        else:
            return JsonResponse({}, safe=False, status=404)

    return redirect('index')
