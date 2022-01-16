from django.urls import path
from . import views

urlpatterns = [
    path('plans', views.PlanView.as_view()),  # 전체 플랜 조회
    path('plans/<int:pk>', views.PlanDetailView.as_view()),  # 특정 플랜 조회
    path('plans/<int:pk>/buy', views.BuyPlanView.as_view()),  # 특정 플랜 구매
    path('plans/<int:pk>/wish', views.WishPlanView.as_view()),  # 특정 플랜 찜하기

    path('myplans/wish', views.WishPlansView.as_view()),  # 유저가 찜한 플랜 조회
    path('myplans/buy', views.BuyPlansView.as_view()),  # 유저가 구매한 플랜 조회
    path('myplans/registered', views.RegisteredPlanView.as_view()),  # 유저가 등록한 플랜 조회
    path('myplans/<int:pk>/register', views.RegisterPlanView.as_view()),  # 구매한 플랜 등록
    path('myplans/<int:pk>/delete', views.DeletePlanView.as_view()),  # 등록한 플랜 삭제
]
