from django.forms import CharField, Form, ModelForm, TextInput, PasswordInput, EmailField, EmailInput, HiddenInput, ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model

from messenger.models import User, Chat, Message


class SignUpForm(UserCreationForm):
    username = CharField(
        label='Логин',
        help_text='Введите логин',
        widget=TextInput(attrs={'id': 'login-field', 'placeholder': 'Введите логин'})
    )

    email = EmailField(
        label='Почта',
        help_text='Введите почту',
        widget=EmailInput(attrs={'id': 'email-field', 'placeholder': 'Введите почту'}),
        required=False
    )

    password1 = CharField(
        label='Пароль',
        help_text='Введите пароль',
        widget=PasswordInput(attrs={'id': 'password-field-1', 'placeholder': 'Введите пароль'})
    )

    password2 = CharField(
        label='Пароль',
        help_text='Повторите пароль',
        widget=PasswordInput(attrs={'id': 'password-field-2', 'placeholder': 'Повторите пароль'})
    )


    class Meta(UserCreationForm.Meta):
        model = get_user_model()

        fields = ['username', 'email', 'password1', 'password2']


class SignInForm(AuthenticationForm):
    username = CharField(
        label='Логин',
        help_text='Введите логин',
        widget=TextInput(attrs={'id': 'login-field', 'placeholder': 'Введите логин'})
    )

    password = CharField(
        label='Пароль',
        help_text='Введите пароль',
        widget=PasswordInput(attrs={'id': 'password-field', 'placeholder': 'Введите пароль'})
    )


class SendMessageForm(ModelForm):
    chat_id = CharField(
        widget=HiddenInput()
    )


    def __init__(self, *args, **kwargs):
        current_chat_id = kwargs.pop('current_chat_id', None)

        super().__init__(*args, **kwargs)

        if current_chat_id:
            self.fields['chat_id'].initial = current_chat_id


    message = CharField(
        label='Сообщение',
        help_text='Введите сообщение',
        widget=TextInput(attrs={'class': 'message-input', 'placeholder': 'Введите сообщение'})
    )


    def clean(self):
        cleaned_data = super().clean()

        id = cleaned_data.get('chat_id')
        chat = Chat.objects.filter(id=id).first()

        if chat is None:
            raise ValidationError('Чата не существует')

        return cleaned_data


    class Meta:
        model = Message

        fields = []


class AddChatForm(ModelForm):
    username = CharField(
        label='Имя пользователя',
        help_text='Введите имя пользователя',
        widget=TextInput(attrs={'class': 'add-chat-input', 'placeholder': 'Введите имя пользователя'})
    )


    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)

        super().__init__(*args, **kwargs)


    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        user = User.objects.filter(username=username).first()

        if user is None:
            raise ValidationError('Пользователя не существует')

        current_user = self.current_user

        if user == current_user:
            raise ValidationError('Нельзя создать чат с самим собой')

        chats = Chat.objects.filter(users=user).filter(users=current_user)

        if chats:
            raise ValidationError('Чат уже существует')

        return cleaned_data


    class Meta:
        model = Chat

        fields = []
