from django.db import models
from django.utils import timezone

# Create your models here.


class Notice(models.Model):
    title = models.CharField(max_length=50)  # 제목
    content = models.TextField()  # 내용
    created_at = models.DateField()  # 생성 날짜
    updated_at = models.DateField()  # 수정 날짜

    def __str__(self):
        return self.title