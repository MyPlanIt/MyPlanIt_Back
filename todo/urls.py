from django.urls import path
from . import views

urlpatterns = [
    path('todos/plan/<str:date>', views.PlanTodoView.as_view()),  # 해당 날짜의 플랜 투두 조회
    path('todos/plan/<int:plan_id>/<int:id>/check', views.CheckPlanTodoView.as_view()),  # 플랜 투두 완료 기능
    path('todos/plan/<int:id>/delay', views.DelayPlanTodoView.as_view()),  # 플랜 투두 미루기 기능
    path('todos/plan/<int:plan_id>/todos', views.PlanTodosView.as_view()),  # 플랜 클릭 시 전체 투두 조회 기능
    path('todos/plan/<int:todo_id>/detail', views.DetailTodoView.as_view()),  # 투두 세부 정보 조회 기능

    path('todos/my/<str:date>', views.MyTodoVIew.as_view()),  # 개인 투두 조회, 추가
    path('todos/my/<int:id>/check', views.EditMyTodoView.as_view()),  # 개인 투두 완료 기능
    path('todos/my/<int:id>/delete', views.EditMyTodoView.as_view()),  # 개인 투두 삭제 기능
    path('todos/my/<int:id>/edit', views.EditMyTodoView.as_view()),  # 개인 투두 이름 변경(수정) 기능
    path('todos/my/<int:id>/delay', views.DelayMyTodoView.as_view())  # 개인 투두 미루기 기능
]
