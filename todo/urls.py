from django.urls import path
from . import views

urlpatterns = [
    path('todos/plan/<str:date>', views.PlanTodoView.as_view()),  # 해당 날짜의 플랜 투두 조회
    path('todos/plan/<int:plan_id>/<int:id>/check', views.CheckPlanTodoView.as_view()),  # 플랜 투두 완료 기능
    path('todos/plan/<int:id>/delay', views.DelayPlanTodoView.as_view()),  # 플랜 투두 미루기 기능
    path('todos/plan/<int:plan_id>/todos', views.PlanTodosView.as_view()),  # 플랜 클릭 시 전체 투두 조회 기능
    path('todos/plan/<int:todo_id>/detail', views.DetailTodoView.as_view()),  # 투두 세부 정보 조회 기능

    # All, Progress, Done
    path('todos/plan/detail/all/<int:plan_id>', views.PlanDetailAllView.as_view()), # 플랜 상세 페이지 중 All 조회 기능
    path('todos/plan/detail/uncheck/<int:plan_id>', views.PlanTodoUncheckView.as_view()), # 플랜 상세 페이지 중 Uncheck 기능
    path('todos/plan/detail/check/<int:plan_id>', views.PlanTodoCheckView.as_view()), # 플랜 상세 페이지 중 Check 기능

    # 미루기, 앞당기기
    path('todos/plan/delay/<int:id>', views.PlanTodoDelayView.as_view()), # 플랜투두 미루기
    path('todos/plan/advance/<int:id>', views.PlanTodoAdvanceView.as_view()), # 플랜투두 앞당기기

    path('todos/my/<str:date>', views.MyTodoVIew.as_view()),  # 개인 투두 조회, 추가
    path('todos/my/<int:id>/check', views.EditMyTodoView.as_view()),  # 개인 투두 완료 기능
    path('todos/my/<int:id>/delete', views.EditMyTodoView.as_view()),  # 개인 투두 삭제 기능
    path('todos/my/<int:id>/edit', views.EditMyTodoView.as_view()),  # 개인 투두 이름 변경(수정) 기능
    path('todos/my/<int:id>/delay', views.DelayMyTodoView.as_view()),  # 개인 투두 미루기 기능
    path('todos/my/<int:id>/advance', views.AdvanceMyTodoView.as_view()),  # 개인 투두 앞당기기 기능

    path('todos/allofdate', views.ShowAllTodosView.as_view())  # 전체 투두 날짜 조회 기능
]
