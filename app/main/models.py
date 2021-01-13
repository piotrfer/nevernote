from django.db import models
from django.contrib.auth.models import User

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_to = models.ManyToManyField(User)
    content = models.TextField()
    attachment = models.FileField()
    is_encrypted = models.BooleanField(default=False)
