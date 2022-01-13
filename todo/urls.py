from django.urls import path, include
from . import views

urlpatterns = [
    path('todo/plan/<str:pk>', views.PlanTodoAPIView.as_view()), # 해당 날짜의 플랜 투두 조회
    path('todo/plan/<int:plan_id>/<int:plan_todo_id>', views.PlanTodoCheckAPIView.as_view()), # 플랜 투두 완료 기능
]