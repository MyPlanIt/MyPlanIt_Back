from django.contrib import admin
from .models import Plan, Plan_todo, Plan_todo_video, User_Plan, User_plan_todo


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    list_display = ['id', 'category', 'name', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())


@admin.register(Plan_todo)
class Plan_todoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'img_url', 'date', 'plan']



@admin.register(Plan_todo_video)
class Plan_todo_videoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'video_url', 'desc', 'plan_todo']


