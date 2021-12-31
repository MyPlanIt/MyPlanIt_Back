# Generated by Django 3.1.14 on 2021-12-31 08:08

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=30)),
                ('realname', models.CharField(max_length=30)),
                ('phone_num', models.CharField(max_length=11)),
                ('auth_num', models.CharField(blank=True, max_length=10, null=True)),
                ('email_agree', models.BooleanField(default=False)),
                ('sns_agree', models.BooleanField(default=False)),
                ('nickname', models.CharField(max_length=20)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'managed': True,
            },
            managers=[
                ('objects', accounts.models.UserManager()),
            ],
        ),
    ]
