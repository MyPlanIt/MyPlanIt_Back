# Generated by Django 3.1.14 on 2022-01-15 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', 'add_user_personal_todo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user_personal_todo',
            name='delete_flag',
        ),
    ]