import jwt.exceptions
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.hashers import check_password

from myplanit.settings import env
from .models import User
from .serializers import SignupSerializer, UserSeriallizer
import jwt


# Create your views here.


def get_user(pk):
    return get_object_or_404(User, pk=pk)


# 회원가입
class SignupView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # 회원가입 이후 첫 토큰 발행
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 회원가입 에러인 경우(email, username 검증에서 탈락 시)


# 로그인
class LoginView(APIView):
    # 토큰으로 유저 정보 조회
    def get(self, request):
        try:
            access_token = request.COOKIES['access_token']
            payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_user(pk)
            serializer = UserSeriallizer(user)
            response = Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
            return response

        # 토큰 만료시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh': request.COOKIES.get('refresh_token', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access_token = serializer.data.get('access', None)
                refresh_token = serializer.data.get('refresh', None)
                payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_user(pk)
                serializer = UserSeriallizer(instance=user)
                response = Response(serializer.data, status=status.HTTP_200_OK)
                response.set_cookie('access_token', access_token)
                response.set_cookie('refresh_token', refresh_token)
                return response

            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

    # 로그인 : access, refresh 토큰 생성
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None: # 해당 email의 user가 존재하지 않는 경우
            return Response(
                {"message": "존재하지않는 email입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password): # 비밀번호에서 틀린 경우
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user is not None: # 모두 성공 시
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": UserSeriallizer(user).data,
                    "message": "login success",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status=status.HTTP_200_OK
            )
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        else: # 그 외
            return Response(
                {"message": "로그인에 실패하였습니다"}, status=status.HTTP_400_BAD_REQUEST
            )


# 온보딩
class OnboardingView(APIView):
    def post(self, request):
        jobs = request.data.get('jobs')
        interests = request.data.get('interests')
        try:
            access_token = request.COOKIES['access_token']
            payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_user(pk)
            print(user)

        # 토큰 만료시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            data = {'refresh': request.COOKIES.get('refresh_token', None)}
            serializer = TokenRefreshSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                access_token = serializer.data.get('access', None)
                refresh_token = serializer.data.get('refresh', None)
                payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
                pk = payload.get('user_id')
                user = get_user(pk)
                response = Response(status=status.HTTP_200_OK)
                response.set_cookie('access_token', access_token)
                response.set_cookie('refresh_token', refresh_token)
            else:
                raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user.jobs = jobs
        user.interests = interests
        user.save()
        return Response({"message": "응답완료"}, status=status.HTTP_200_OK)