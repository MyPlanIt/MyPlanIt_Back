# Generated by Django 3.1.14 on 2022-04-01 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_proposal'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_plan_todo',
            name='day',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
