from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User
import datetime

CATEGORY_CHOICES = (('Routine', 'Routine'),
                    ('Growth', 'Growth'))


class Plan(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)  # 루틴 / 성장
    main_img_url = models.URLField()
    name = models.CharField(max_length=30)
    price = models.PositiveIntegerField(default=0)
    writer_name = models.CharField(max_length=20)
    writer_img = models.URLField(blank=True, null=True)
    writer_intro = models.CharField(max_length=30)
    intro_img_url = models.URLField()  # 플랜 클릭 시 보여줘야 할 이미지파일
    desc = models.TextField()
    tags = TaggableManager(blank=True)  # 태그

    def __str__(self):
        return self.name


class Proposal(models.Model):
    proposal = models.TextField()


class Plan_todo(models.Model):
    name = models.CharField(max_length=30)
    img_url = models.URLField(blank=True, null=True)
    media_flag = models.BooleanField(default=0)
    date = models.PositiveIntegerField(default=0)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Plan_todo_video(models.Model):
    title = models.CharField(max_length=30)
    video_url = models.URLField()
    desc = models.TextField()
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_todo = models.ForeignKey(Plan_todo, on_delete=models.CASCADE)


# 중개 모델들 #
class User_Plan(models.Model):
    wish_flag = models.BooleanField(default=False)  # 찜하기
    register_flag = models.BooleanField(default=False)  # 등록
    own_flag = models.BooleanField(default=False)  # 소유
    finish_flag = models.BooleanField(default=False)
    rate = models.IntegerField(default=0)  # 달성률

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    start_date = models.DateField(default=datetime.date.today())
    finish_date = models.DateField(default=datetime.date.today())

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


class User_plan_todo(models.Model):
    finish_flag = models.BooleanField(default=False)
    date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    plan_todo = models.ForeignKey(Plan_todo, on_delete=models.CASCADE)
    day = models.PositiveIntegerField(default=0) # 일차
