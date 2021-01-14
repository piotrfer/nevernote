from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Note
from .forms import NoteForm
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto import Random
from django.db.models import Q

""" VIEWS """
def notes(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    notes = Note.objects.filter(user = request.user)
    public_notes = Note.objects.filter(Q(is_public = True) & ~Q(user = request.user))

    return render(request, "notes-list.html", { "notes" : notes, "public_notes" : public_notes })

def create_note(request):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    if request.method == 'POST':
        data = dict(request.POST)
        if "is_encrypted" in data and data["is_encrypted"] == ["on"]:
            if not process_encrypted(request, data):
                return redirect("create-note")
            
            else:
                return redirect("notes-list")
        else:
            if not process_unencrypted(request, data):
                return redirect("create-note")
            
            else:
                return redirect("notes-list")
        
    elif request.method == 'GET':
        return render(request, "create-note.html")

def show_note(request, id):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    public_note = False
    notes = Note.objects.filter(user = request.user, id = id)
    if len(notes) == 0:
        notes = Note.objects.filter(is_public=True, id = id)
        if len(notes) == 0:
            messages.add_message(request, messages.ERROR, "Note does not exist")
            return redirect("home")
        else:
            note = notes[0]
            public_note = True
    else:
        note = notes[0]
    
    if request.method == 'GET':
        if note.is_encrypted:
            return render(request, "show-note.html", {"note" : '', "encrypted" : True, "public" : public_note })
        else:
            return render(request, "show-note.html", {"note" : note, "encrypted" : False, "public" : public_note })
    
    if request.method == 'POST':
        data = request.POST
        password = data["password_text"]
        
        if not password:
            messages.add_message(request, messages.ERROR, "You have to provide password!")
            return redirect("notes-list")
        
        note = decrypt_note(password, note)
        return render(request, "show-note.html", { "note" : note, "encrypted" : False })
        

def edit_note(request, id):
    if not request.user.is_authenticated:
        return unauthorized(request)
    
    notes = Note.objects.filter(user = request.user, id = id)
    
    if len(notes) == 0:
        messages.add_message(request, messages.ERROR, "Note does not exist")
        return redirect("home")
    
    note = notes[0]
    if note.is_encrypted:
        messages.add_message(request, messages.ERROR, "You cannot edit encrypted notes. Try adding new one.")
        return redirect(f"/notes/{id}/show")

    if request.method == 'GET':
        form = NoteForm(initial={ "content" : note.content, "is_public" : note.is_public})
        return render(request, "edit-note.html", {"form" : form })

    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note.content = form.cleaned_data["content"]
            note.is_public = form.cleaned_data["is_public"]
            note.save()
            messages.add_message(request, messages.SUCCESS, "Changes were saved")
            return redirect('notes-list')
        else:
            messages.add_message(request, messages.ERROR, "Form is invalid!")
            return redirect("edit-note", id=note.id)

def delete_note(request, id):
    if not request.user.is_authenticated:
        return unauthorized(request)

    notes = Note.objects.filter(user = request.user, id = id)
    
    if len(notes) == 0:
        messages.add_message(request, messages.ERROR, "Note does not exist")
        return redirect("home")
    
    note = notes[0]

    if request.method == 'GET':
        return render(request, "delete-note.html")
    
    if request.method == 'POST':
        note.delete()
        messages.add_message(request, messages.SUCCESS, "Note was deleted")
        return redirect('notes-list')



""" REDIRECTS """        

def unauthorized(request):
    messages.add_message(request, messages.ERROR, 'You are not authorized to view this page!')
    return redirect("landing-page")



""" FUNCTIONS """
def process_encrypted(request, data):
    print(data)
    if "content" not in data or data["content"] == [""]:
        messages.add_message(request, messages.ERROR, "Content cannot be empty!")
        return False
    
    content = data["content"][0]
    
    if "password_text" not in data or data["password_text"] == [""]:
        messages.add_message(request, messages.ERROR, "Password cannot be empty!")
        return False

    password = data["password_text"][0]
    
    if "is_public" in data and data["is_public"] == ["on"]:
        messages.add_message(request, messages.ERROR, "You cannot share encrypted notes!")
        return False
    
    encrypted_content = encrypt_content(content, password)
    note = Note(
        user = request.user,
        content = 'ENCRYPTED NOTE',
        is_encrypted = True,
        encrypted_content = encrypted_content,
        is_public = False
    )
    note.save()
    messages.add_message(request, messages.SUCCESS, "Encrypted note was created!")
    return True


def process_unencrypted(request, data):
    print(data)
    if "content" not in data or data["content"] == [""]:
        messages.add_message(request, messages.ERROR, "Content cannot be empty!")
        return False

    is_public = False
    if "is_public" in data and data["is_public"] == ["on"]:
        is_public = True

    content = data["content"][0]
    note = Note(
        user = request.user,
        content = str(content),
        is_encrypted = False,
        is_public = is_public
    )
    note.save()
    messages.add_message(request, messages.SUCCESS, "Note was created!")
    return True


""" ENCRYPTION """
""" using https://www.quickprogrammingtips.com/ """

BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

def encrypt_content(content, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    content = pad(content)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(content.encode("utf-8")))
 
 
def decrypt(encrypted, password):
    private_key = hashlib.sha256(password.encode("utf-8")).digest()
    encrypted = base64.b64decode(encrypted)
    iv = encrypted[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted[16:]))



def decrypt_note(password, note):
    note.content = decrypt(note.encrypted_content, password)
    try:
        note.content = note.content.decode("utf-8")
    except:
        pass
    return note