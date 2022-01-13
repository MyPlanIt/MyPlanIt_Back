from rest_framework import serializers
from plan.models import Plan, Plan_todo, Plan_todo_video, User_Plan, User_plan_todo


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'rate']


class UserPlanTodoSerializer(serializers.ModelSerializer):
    #plan = serializers.SerializerMethodField() # serializer method field 이용
    plan_todo = serializers.SerializerMethodField() # serializer method field 이용
    plan_id = serializers.SerializerMethodField()
    plan_todo_id = serializers.SerializerMethodField()

    #def get_plan(self, obj):
    #    return obj.plan.name

    def get_plan_todo(self, obj):
        return obj.plan_todo.name

    def get_plan_id(self, obj):
        return obj.plan.id

    def get_plan_todo_id(self, obj):
        return obj.plan_todo.id

    class Meta:
        model = User_plan_todo
        fields = ['id', 'plan_id', 'plan_todo_id', 'plan_todo', 'finish_flag', 'date']


class PlanTodoSerializer(serializers.ModelSerializer):
    plan_todo_id = serializers.SerializerMethodField()
    plan_todo = serializers.SerializerMethodField()

    def get_plan_todo_id(self, obj):
        return obj.plan_todo.id

    def get_plan_todo(self, obj):
        return obj.plan_todo.name

    class Meta:
        model = User_plan_todo
        fields = ['id', 'plan_todo_id', 'plan_todo', 'finish_flag']