from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Note
from .forms import NoteForm

# Create your views here.
def notes(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    notes = Note.objects.filter(user = request.user)
    return render(request, "notes-list.html", { "notes" : notes })

def create_note(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = Note(user = request.user,
                        #attachment = form.cleaned_data["attachment"],
                        content = form.cleaned_data["content"])
            note.save()
            messages.add_message(request, messages.SUCCESS, "Note has been created")
            return redirect("notes-list")
        else:
            for error_name in form.error_messages:
                messages.add_message(request, messages.ERROR, form.error_messages[error_name])
            return redirect("create-note")

    elif request.method == 'GET':
        form = NoteForm()
        return render(request, "create-note.html", {"form" : form})

def show_note(request, id):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    note = Note.objects.filter(user = request.user, id = id)[0]
    if not note:
        messages.add_message(request, messages.ERROR, "Note does not exist")
        return redirect("home")
    else:
        return render(request, "show-note.html", {"note" : note })


def edit_note(request, id):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    note = Note.objects.filter(user = request.user, id = id)[0]
    
    if request.method == 'GET':
        if not note:
            messages.add_message(request, messages.ERROR, "Note does not exist")
            return redirect("home")
        else:
            form = NoteForm(initial={"content" : note.content})
            return render(request, "edit-note.html", {"form" : form })

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note.content = form.cleaned_data["content"]
            note.save()
            messages.add_message(request, messages.SUCCESS, "Changes were saved")
            return redirect('notes-list')
        else:
            for error_name in form.error_messages:
                messages.add_message(request, messages.ERROR, form.error_messages[error_name])
            return redirect("edit-note")

def delete_note(request, id):
    if not request.user.is_authenticated:
        return unauthorized(request)

    note = Note.objects.filter(user = request.user, id = id)[0]

    if request.method == 'GET':
        if not note:
            messages.add_message(request, messages.ERROR, "Note does not exist")
            return redirect("home")
        else:
            return render(request, "delete-note.html")
    
    if request.method == 'POST':
        note.delete()
        messages.add_message(request, messages.SUCCESS, "Note was deleted")
        return redirect('notes-list')
        

def unauthorized(request):
    messages.add_message(request, messages.ERROR, 'You are not authorized to view this page!')
    return redirect("landing-page")
