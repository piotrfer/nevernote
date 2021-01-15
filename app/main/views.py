from django.shortcuts import render, redirect
from django.contrib import messages


def index(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    return render(request, "home.html", {})


def landing(request):
    return render(request, "landing.html", {})


def profile(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    return render(request, "my-profile.html")


def unauthorized(request):
    messages.add_message(request, messages.ERROR,
                         'You are not authorized to view this page!')
    return redirect("landing-page")
