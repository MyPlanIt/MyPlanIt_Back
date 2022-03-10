from django.contrib import admin
from .models import landingPage

# Register your models here.


@admin.register(landingPage)
class landingpageAdmin(admin.ModelAdmin):
    list_display = ['id', 'job', 'phoneNum', 'todoPlan', 'created_at']
    list_display_links = ['id', 'job']
    list_filter = ['job', 'todoPlan']