from django.shortcuts import redirect, HttpResponse, render
from django.http import JsonResponse
import requests
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken
import os, environ

User = get_user_model()

env = environ.Env(
    DEBUG=(bool, False)
)
BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))


# JWT 발급 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


class HelloView(APIView):
    def get(self, request):
        user = request.user
        print(user)
        content = {'message': 'Hello, World!'}
        return Response(content)


# code 요청 -> 프론트 부분
@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_login(request):
    app_rest_api_key = "41a2c19cd51500b22e399c7019defd4c"
    # redirect_uri = "http://127.0.0.1:8000/login/kakao/callback"
    redirect_uri = "https://myplanit.link/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


# 카카오 회원가입 & 로그인
@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_callback(request):
    app_rest_api_key = "41a2c19cd51500b22e399c7019defd4c"
    # redirect_uri = "http://127.0.0.1:8000/login/kakao/callback"
    redirect_uri = "https://myplanit.link/login/kakao/callback"
    # client_secret = env('SECRET')
    code = request.GET.get('code')

    token_req = requests.get(
        f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={app_rest_api_key}&redirect_uri={redirect_uri}&code={code}"
    )
    token_req_json = token_req.json()
    access_token = token_req_json.get("access_token")
    refresh_token = token_req_json.get("refresh_token")
    print("access_token: ", access_token)
    print("refresh_token: ", refresh_token)

    kakao_api_response = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    kakao_api_response = kakao_api_response.json()
    user_id = kakao_api_response.get('id')
    #if user_id is None:
    #    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    username = f'user{user_id}'

    realname = kakao_api_response.get('properties').get('nickname')
    print(username, realname)

    try:
        user = User.objects.get(username=username)
        print("기존 유저")

    except:
        user = User(username=username, realname=realname)
        user = user.save()
        user = User.objects.get(username=username)
        print("새로운 유저")

    data = {'username': username, 'token': get_tokens_for_user(user), 'kakao_accessToken': access_token}
    print(data)
    return Response(data, status=200)


# 로그아웃 -> 사용자의 access_token, refresh_token 모두 만료시킴
def kakao_logout(request):
    access = "2zqeoqTJQ-u-a1SiB1ga2SnPv2LIX8OiSQ5oego9cxgAAAF_LK3m6g"
    data = requests.post("https://kapi.kakao.com/v1/user/logout",
                  headers={"Authorization": f"Bearer {access}"},
                  )
    print(data.json())
    return HttpResponse("로그아웃")


# 연결 끊기 -> 사용자와 앱의 연결을 해제(카카오 로그인을 통해 서비스에 가입한 사용자가 탈퇴하거나, 카카오 로그인 연동 해제를 요청할 경우)
def kakao_resign(request):
    access = "eGF4UFcPyV47RB1LNwEHU8vI5Z2EdYHbk1-p1AopcFEAAAF_LNv1Ag"
    data = requests.post("https://kapi.kakao.com/v1/user/unlink",
                         headers={"Authorization": f"Bearer {access}"},
                         )
    print(data.json())
    return HttpResponse("연결종료")


######################## 기존
# 회원가입
class SignupView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        try:
            email = request.data['email']
            password = request.data['password']
            realname = request.data['realname']
            username = request.data['username']
            email_agree = request.data['email_agree']
            sns_agree = request.data['sns_agree']

            if User.objects.filter(email=email).exists() and User.objects.filter(username=username).exists():
                return Response({"message": "email과 username이 모두 존재합니다."}, status=status.HTTP_207_MULTI_STATUS)

            if User.objects.filter(email=email).exists():
                return Response({"message": "email이 이미 존재합니다."}, status=status.HTTP_200_OK)
            if User.objects.filter(username=username).exists():
                return Response({"message": "nickname이 이미 존재합니다."}, status=status.HTTP_202_ACCEPTED)

            user = User(
                email=email,
                realname=realname,
                username=username,
                email_agree=email_agree,
                sns_agree=sns_agree
            )
            user.set_password(password)
            user.save()
            return Response({"message": "회원가입 완료"}, status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 로그인
class LoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:  # 해당 email의 user가 존재하지 않는 경우
            return Response(
                {"message": "존재하지않는 email입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password):  # 비밀번호에서 틀린 경우
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        try:
            # email, password 모두 만족 시
            user_email = authenticate(email=email, password=password)
            user = User.objects.get(email=user_email)

            #payload = JWT_PAYLOAD_HANDLER(user)
            #jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            #data = {'token': jwt_token}
            data = {}
            return Response(data, status=status.HTTP_200_OK)

        except:  # 그 외
            return Response(data={"message": "로그인에 실패하였습니다"}, status=status.HTTP_404_NOT_FOUND)


# 온보딩
class OnboardingView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        jobs = request.data.get('jobs')
        interests = request.data.get('interests')

        try:
            user = request.user
            user.jobs = jobs
            user.interests = interests
            user.save()
            return Response({"message": "success"}, status=status.HTTP_200_OK)

        except:
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)