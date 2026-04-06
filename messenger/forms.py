from django.forms import CharField, TextInput, PasswordInput, EmailField, EmailInput
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
        widget=EmailInput(attrs={'id': 'email-field', 'placeholder': 'Введите почту'})
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
