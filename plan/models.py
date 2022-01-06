from django.db import models
from taggit.managers import TaggableManager
from accounts.models import User

CATEGORY_CHOICES = (('Routine', 'Routine'),
                    ('Growth', 'Growth'))


class Plan(models.Model):
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=30)  # 루틴 / 성장
    category_detail = models.CharField(max_length=30)
    main_img = models.ImageField(upload_to='main_img/', blank=True, null=True)
    name = models.CharField(max_length=30)
    period = models.IntegerField()
    price = models.PositiveIntegerField(default=0)
    plan_writer = models.CharField(max_length=20)
    intro_img = models.ImageField(upload_to='intro_img/', blank=True, null=True)
    tags = TaggableManager(blank=True)

    def __str__(self):
        return self.name


class Plan_todo(models.Model):
    name = models.CharField(max_length=30)
    img = models.ImageField(upload_to='plan_todo_img/', blank=True, null=True)
    date = models.PositiveIntegerField(default=0)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Plan_todo_video(models.Model):
    title = models.CharField(max_length=30)
    video = models.FileField(upload_to="plan_todo_video/", blank=True, null=True)
    desc = models.TextField()
    plan_todo = models.ForeignKey(Plan_todo, on_delete=models.CASCADE)


### 중개 모델들 ###
class User_Plan(models.Model):
    wish_flag = models.BooleanField(default=False)  # 찜하기
    register_flag = models.BooleanField(default=False)  # 등록
    own_flag = models.BooleanField(default=False)  # 소유
    finish_flag = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)


class User_plan_todo(models.Model):
    finish_flag = models.BooleanField(default=False)
    date = models.DateField()

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_todo = models.ForeignKey(Plan_todo, on_delete=models.CASCADE)
