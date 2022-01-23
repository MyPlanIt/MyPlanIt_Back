from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.SignupView.as_view()),  # 회원 가입
    path('login', views.LoginView.as_view()),  # 로그인
    path('signup/onboarding', views.OnboardingView.as_view()),  # 온보딩
]