# Generated by Django 3.1.14 on 2022-01-06 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20220104_1810'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='phone_num',
        ),
    ]