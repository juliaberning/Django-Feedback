# Generated by Django 5.1.1 on 2024-11-01 19:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_userprofile_name_userprofile_surname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='surname',
        ),
    ]