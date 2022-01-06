# Generated by Django 3.1.14 on 2022-01-06 13:57

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0002_auto_20220104_1810'),
        ('taggit', '0003_taggeditem_add_unique_index'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Routine', 'Routine'), ('Growth', 'Growth')], max_length=30)),
                ('category_detail', models.CharField(max_length=30)),
                ('main_img', models.ImageField(blank=True, null=True, upload_to='main_img/')),
                ('name', models.CharField(max_length=30)),
                ('period', models.IntegerField()),
                ('price', models.PositiveIntegerField(default=0)),
                ('plan_writer', models.CharField(max_length=20)),
                ('intro_img', models.ImageField(blank=True, null=True, upload_to='intro_img/')),
                ('tags', taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
        ),
        migrations.CreateModel(
            name='Plan_todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('img', models.ImageField(blank=True, null=True, upload_to='plan_todo_img/')),
                ('date', models.PositiveIntegerField(default=0)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
            ],
        ),
        migrations.CreateModel(
            name='User_plan_todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish_flag', models.BooleanField(default=False)),
                ('date', models.DateTimeField()),
                ('plan_todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan_todo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='User_Plan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wish_flag', models.BooleanField(default=False)),
                ('register_flag', models.BooleanField(default=False)),
                ('own_flag', models.BooleanField(default=False)),
                ('finish_flag', models.BooleanField(default=False)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='Plan_todo_video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('video', models.FileField(blank=True, null=True, upload_to='plan_todo_video/')),
                ('desc', models.TextField()),
                ('plan_todo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plan.plan_todo')),
            ],
        ),
    ]