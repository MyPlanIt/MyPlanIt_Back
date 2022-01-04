# Generated by Django 3.1.14 on 2022-01-04 09:10

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='interests',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, '운동 & 건강'), (2, '자격증'), (3, '코딩 공부'), (4, '디자인'), (5, '관심분야1'), (6, '관심분야2')], max_length=11, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='jobs',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[(1, '대학생'), (2, '취준생'), (3, '주니어 직장인'), (4, '시니어 직장인')], max_length=7, null=True),
        ),
    ]
