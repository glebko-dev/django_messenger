from django.shortcuts import render, redirect


def index(request):
    if request.user.is_authenticated:
        pass

    return redirect('sign_in')


def sign_in(request):
    if request.method == 'POST':
        pass

    return render(request, 'sign_in.html')


def sign_up(request):
    if request.method == 'POST':
        pass

    return render(request, 'sign_up.html')
