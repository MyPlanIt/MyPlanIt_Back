from django.db import models

# Create your models here.


class landingPage(models.Model):
    phoneNum = models.CharField(max_length=20)  # 전화번호(필수)
    job = models.CharField(max_length=20)  # 직업(필수)
    todoPlan = models.TextField(blank=True)  # 원하는 TO-DO 플랜(선택)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성시간(자동)