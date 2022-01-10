from django.urls import path
from . import views

urlpatterns = [
    path('plan', views.PlanView.as_view()),
    path('plan/<int:pk>', views.PlanDetailView.as_view()),
    path('plan/<int:pk>/buy', views.PlanBuyView.as_view()),
    path('plan/<int:pk>/wish', views.PlanWishView.as_view()),
    path('myplan', views.WishPlanView.as_view()),
    path('myplan/buy', views.OwnPlanView.as_view()),

    path('plan/<int:pk>/register', views.RegiserPlanView.as_view()),
]