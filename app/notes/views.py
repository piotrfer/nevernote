from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Note
from .forms import NoteForm
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
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
    
    nonce = get_random_bytes(16)
    encrypted_content = encrypt_content(password, content, nonce)
    encrypted_password = b'there will be password encryption here'
    note = Note(
        user = request.user,
        content = 'ENCRYPTED NOTE',
        is_encrypted = True,
        encrypted_content = encrypted_content,
        nonce = nonce,
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
def fill_password(password, nonce):
    print(f"password: {password}")
    print(f"nonce: {nonce}")
    dk = PBKDF2(password, nonce, 16, 10000)
    print(f"result: {dk}")
    return dk

def encrypt_content(password, content, nonce):
    filled_password = fill_password(password, nonce)
    print(filled_password)
    aes = AES.new(filled_password, AES.MODE_CFB, nonce)
    encrypted_content = aes.encrypt(content.encode('utf-8'))
    return encrypted_content

def decrypt_note(password, note):
    nonce = note.nonce.tobytes()
    filled_password = fill_password(password, nonce)
    print(filled_password)
    aes = AES.new(filled_password, AES.MODE_CFB, nonce)
    try:
        decrypted_content = aes.decrypt(note.encrypted_content.tobytes())
        note.content = decrypted_content.decode('utf-8')
    except:
        note.content = decrypted_content
    
    return note