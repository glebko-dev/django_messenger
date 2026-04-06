from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from messenger.forms import SignUpForm, SignInForm


def index(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')

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
