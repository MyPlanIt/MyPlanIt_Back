from django.urls import path, include
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view()),
    path('login', views.LoginView.as_view()),
]