from django.urls import path, include
from . import views

urlpatterns = [
    path('todos/plan/<str:pk>', views.PlanTodoAPIView.as_view()), # 해당 날짜의 플랜 투두 조회
    path('todos/plan/<int:plan_id>/<int:plan_todo_id>', views.PlanTodoCheckAPIView.as_view()),  # 플랜 투두 완료 기능
    path('todos/plan/<int:plan_todo_id>/delay', views.PlanTodoDelayAPIView.as_view()),  # 플랜 투두 미루기 기능
    path('todos/plan/<int:plan_id>/todos', views.AllTodoAPIView.as_view()),  # 플랜 클릭 시 전체 투두 조회 기능
    path('todos/plan/<int:plan_todo_id>/detail', views.DetailTodoAPIView.as_view()),  # 투두 세부 정보 조회 기능

    path('todos/my/<str:date>', views.PersonalTodoAPIVIew.as_view()),  # 개인 투두 조회, 추가
    path('todos/my/<int:id>/check', views.PersonalTodoCheckAPIView.as_view()),  # 개인 투두 완료 기능
    path('todos/my/<int:id>/delete', views.PersonalTodoDeleteAPIView.as_view()),  # 개인 투두 삭제 기능
    path('todos/my/<int:id>/edit', views.PersonalTodoEditAPIView.as_view()),  # 개인 투두 수정 기능
    path('todos/my/<int:id>/delay', views.PersonalTodoDelayAPIView.as_view())  # 개인 투두 미루기 기능
]