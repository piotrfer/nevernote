from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "You have been registered!")
            return redirect("login")
        else:
            for error_name in form.error_messages:
                messages.add_message(request, messages.ERROR, form.error_messages[error_name])
            return redirect("register")
    else:
        form = RegisterForm()
    
    return render(request, "register.html", { "form" : form })
