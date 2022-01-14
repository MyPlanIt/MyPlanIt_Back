from django.contrib import admin
from .models import Plan, Plan_todo, Plan_todo_video, User_Plan, User_plan_todo


class Plan_todo_videoInline(admin.TabularInline):
    model = Plan_todo_video


class Plan_todoInline(admin.TabularInline): # Plan_todo를 inline으로 설정
    model = Plan_todo
    inlines = [Plan_todo_videoInline, ]


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    inlines = [Plan_todoInline, Plan_todo_videoInline] # Plan_todo를 Plan의 Inline으로 설정
    list_display = ['id', 'category', 'name', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())


@admin.register(Plan_todo_video)
class Plan_todo_videoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'video_url', 'desc', 'plan_todo']


@admin.register(User_Plan)
class User_PlanAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'wish_flag', 'register_flag', 'own_flag', 'finish_flag', 'rate']


@admin.register(User_plan_todo)
class User_plan_todoAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'plan_todo', 'finish_flag', 'date']