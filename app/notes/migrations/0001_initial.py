# Generated by Django 2.1.15 on 2021-01-13 19:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EncryptedNote',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('encrypted_content', models.BinaryField()),
                ('encrypted_attachment', models.FileField(blank=True, null=True, upload_to='')),
                ('created_on', models.TimeField(auto_now=True)),
                ('password', models.CharField(max_length=50)),
                ('shared_to', models.ManyToManyField(related_name='encrypted_shared_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('attachment', models.FileField(blank=True, null=True, upload_to='')),
                ('created_on', models.TimeField(auto_now=True)),
                ('shared_to', models.ManyToManyField(related_name='shared_users', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
