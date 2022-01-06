from django.contrib import admin
from taggit.models import (
    TagBase, TaggedItemBase
)

# Register your models here.

from django.contrib import admin
from .models import Plan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    filter_horizontal = ['tags']
    list_display = ['id', 'category', 'name', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())



