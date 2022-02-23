# Generated by Django 3.1.14 on 2022-02-22 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='email_agree',
        ),
        migrations.RemoveField(
            model_name='user',
            name='interests',
        ),
        migrations.RemoveField(
            model_name='user',
            name='jobs',
        ),
        migrations.RemoveField(
            model_name='user',
            name='sns_agree',
        ),
        migrations.AlterField(
            model_name='user',
            name='realname',
            field=models.CharField(max_length=20),
        ),
    ]