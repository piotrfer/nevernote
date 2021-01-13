from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.urls import reverse


def register(response):
    if response.method == 'POST':
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
        return redirect(reverse("login"))
    else:
        form = RegisterForm()
    
    return render(response, "register.html", { "form" : form })
