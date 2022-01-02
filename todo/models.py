from django.db import models


class TimeStampedModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Personal_todo(TimeStampedModel):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='personal_todo')
    todo_name = models.CharField(max_length=50)
    date = models.DateTimeField()
    tag = models.CharField(max_length=20)
    finish_flag = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['todo_name', 'date']

    class Meta:
        verbose_name = 'Todo'
        verbose_name_plural = 'Todos'
        ordering = ['-created_on']

    def __str__(self):
        return self.todo_name

    def get_user(self):
        return self.user
