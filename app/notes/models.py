import uuid
from django.db import models
from django.contrib.auth.models import User


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_public = models.BooleanField(default=False)
    content = models.TextField()
    created_on = models.TimeField(auto_now=True)

    is_encrypted = models.BooleanField(default=False)
    encrypted_content = models.BinaryField(blank=True, null=True)

    # add files some day
