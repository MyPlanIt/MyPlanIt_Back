from django.urls import path
from . import views

urlpatterns = [
    path('landingpage/register', views.landingpageView.as_view()),  # 전체 플랜 조회
]