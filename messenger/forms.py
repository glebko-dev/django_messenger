from django.forms import CharField, Form, TextInput, PasswordInput, EmailField, EmailInput, HiddenInput
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model


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


class SendMessageForm(Form):
    username = CharField(
        widget=HiddenInput()
    )

    message = CharField(
        label='Сообщение',
        help_text='Введите сообщение',
        widget=TextInput(attrs={'class': 'message-input', 'placeholder': 'Введите сообщение'})
    )


class AddChatForm(Form):
    username = CharField(
        label='Имя пользователя',
        help_text='Введите имя пользователя',
        widget=TextInput(attrs={'class': 'add-chat-input', 'placeholder': 'Введите имя пользователя'})
    )
