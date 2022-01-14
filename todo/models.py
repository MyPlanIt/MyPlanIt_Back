from django.db import models
from accounts.models import User


class User_personal_todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=100)
    date = models.DateField()
    finish_flag = models.BooleanField(default=False)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_name