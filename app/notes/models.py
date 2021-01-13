import uuid
from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_to = models.ManyToManyField(User,related_name="shared_users")
    content = models.TextField()
    # will have to migrate to binary
    attachment = models.FileField(blank=True, null=True)
    created_on = models.TimeField(auto_now=True)


class EncryptedNote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_to = models.ManyToManyField(User,related_name="encrypted_shared_users")
    encrypted_content = models.BinaryField()
    # will have to migrate to binary
    encrypted_attachment = models.FileField(blank=True, null=True)
    created_on = models.TimeField(auto_now=True)
    password = models.CharField(max_length=50)