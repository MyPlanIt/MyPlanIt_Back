from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('plan.urls')),
    path('', include('todo.urls')),
    path('', include('landingpage.urls')),
    path('', include('info.urls')),
]
