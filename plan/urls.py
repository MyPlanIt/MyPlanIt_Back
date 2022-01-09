from django.urls import path
from . import views

urlpatterns = [
    path('plan/', views.PlanView.as_view()),
    path('plan/<int:pk>', views.PlanDetailView.as_view()),
    path('plan/<int:pk>/buy', views.PlanBuyView.as_view()),
    path('myplan/', views.OwnPlanView.as_view()),
]