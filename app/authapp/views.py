from django.shortcuts import render, redirect
from .forms import RegisterForm, AuthenticationForm as LoginForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib import messages
import time

LOGIN_DELAY_S = 1
SESSION_EXPIRY_S = 300


def login(request):
    if request.user.is_authenticated:
        return already_authorized(request)
    if request.method == 'GET':
        form = LoginForm()
        return render(request, "login.html", {"form": form})
    if request.method == 'POST':
        time.sleep(LOGIN_DELAY_S)
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password'))
            if user is not None:
                login_user(request, user)
                return redirect("home")

        messages.add_message(request, messages.ERROR,
                             "Invalid login or password")
        return redirect("login")


def register(request):
    if request.user.is_authenticated:
        return already_authorized(request)
    if request.method == 'POST':
        time.sleep(LOGIN_DELAY_S)
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS,
                                 "You have been registered!")
            return redirect("login")
        else:
            for error_name in form.error_messages:
                messages.add_message(
                    request, messages.ERROR, form.error_messages[error_name])
            return redirect("register")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def logout(request):
    logout_user(request)
    return redirect("landing-page")


def already_authorized(request):
    messages.add_message(request, messages.ERROR, "You are already logged in!")
    return redirect("home")
