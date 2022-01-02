from django.urls import path, include
from . import views

urlpatterns = [
    path('todo/<int:pk>', views.PersonalTodoView.as_view()),
]