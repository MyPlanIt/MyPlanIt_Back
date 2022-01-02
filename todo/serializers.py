from rest_framework import serializers

from .models import Personal_todo


class PersonalTodoSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format='%Y-%m-%d')

    class Meta:
        model = Personal_todo
        fields = ['id', 'todo_name', 'date', 'tag', 'finish_flag']
