from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:pk>/todo', views.PersonalTodoView.as_view()),
]