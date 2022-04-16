from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenVerifyView
from accounts.views import views
from accounts.views import googleviews
from accounts.views import kakaoviews

urlpatterns = [
    ## 기존
    # path('signup', views.SignupView.as_view()),  # 회원 가입
    # path('login', views.LoginView.as_view()),  # 로그인
    # path('signup/onboarding', views.OnboardingView.as_view()),  # 온보딩

    ## 새로 도입
    path('api/token', jwt_views.TokenObtainPairView.as_view()),
    path('api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/refresh', jwt_views.TokenRefreshView.as_view()),  # access-token refresh

    # 카카오 소셜로그인
    # path('auth/kakao', views.kakao_login, name='kakao_login'), # 프론트 부분
    path('auth/kakao', kakaoviews.kakao_callback, name='kakao_callback'),  # 백엔드 부분
    path('logout/kakao', kakaoviews.kakao_logout, name="kakao_logout"),
    path('resign/kakao', kakaoviews.kakao_resign, name="kakao_resign"),

    # 구글 소셜로그인
    path('auth/google', googleviews.google_callback, name='google_login_callback'),
    path('logout/google', googleviews.google_logout, name='google_logout'),

    # 관리자 인증
    path('manager', kakaoviews.login, name='login'),
]
