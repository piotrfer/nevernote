from django.shortcuts import render, redirect

def index(response):
    if not response.user.is_authenticated:
        return unauthorized()
    return render(response, "home.html", {})

def landing(response):
    return render(response, "landing.html", {})

def notes(response):
    if not response.user.is_authenticated:
        return unauthorized()
    return render(response, "notes-list.html")

def profile(response):
    if not response.user.is_authenticated:
        return unauthorized()
    return render(response, "my-profile.html")


def unauthorized():
    return redirect("/", { "messages" : ["message1", "message2"]})