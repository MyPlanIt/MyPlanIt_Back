from django.urls import path
from . import views

urlpatterns = [
    path('notice', views.NoticeView.as_view()),  # 공지
]
