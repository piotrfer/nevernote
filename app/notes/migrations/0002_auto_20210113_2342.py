# Generated by Django 2.1.15 on 2021-01-13 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encryptednote',
            name='shared_to',
        ),
        migrations.RemoveField(
            model_name='note',
            name='attachment',
        ),
        migrations.AddField(
            model_name='note',
            name='encrypted_content',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='is_encrypted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='note',
            name='password',
            field=models.BinaryField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='encryptednote',
            name='password',
            field=models.BinaryField(),
        ),
    ]