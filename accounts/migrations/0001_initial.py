# Generated by Django 3.1.14 on 2022-01-21 04:14

import accounts.models
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=30, unique=True)),
                ('realname', models.CharField(max_length=30)),
                ('email_agree', models.BooleanField(default=False)),
                ('sns_agree', models.BooleanField(default=False)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('jobs', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('대학생', '대학생'), ('취준생', '취준생'), ('주니어 직장인', '주니어 직장인'), ('시니어 직장인', '시니어 직장인')], max_length=23, null=True)),
                ('interests', multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('lang_en', '영어'), ('lang_zh', '중국어'), ('lang_ja', '일본어'), ('lang_es', '스페인어'), ('life_fa', '패션'), ('life_be', '뷰티'), ('life_ac', '연기'), ('life_da', '춤'), ('com_co', '코딩'), ('com_da', '데이터 분석'), ('com_ed', '영상 편집'), ('ge_cu', '요리'), ('ge_ex', '운동'), ('ge_ca', '캘리그라피'), ('ge_ge', '교양'), ('art_mu', '음악'), ('art_cr', '공예'), ('art_ph', '사진'), ('art_pd', '영상 제작'), ('art_de', '디자인'), ('art_ar', '미술'), ('bus_ft', '재테크'), ('bus_fin', '파이낸스'), ('bus_ma', '마케팅'), ('bus_hr', 'HR'), ('bus_sa', '영업')], max_length=186, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
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
