from django.shortcuts import redirect, HttpResponse
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from myplanit.settings.base import env

User = get_user_model()


# JWT 발급 함수
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
    }


# code 요청 -> 프론트 부분
@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_login(request):
    app_rest_api_key = "41a2c19cd51500b22e399c7019defd4c"
    redirect_uri = "https://myplanit.link/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={app_rest_api_key}&redirect_uri={redirect_uri}&response_type=code"
    )


# 카카오 회원가입 & 로그인
@api_view(['GET'])
@permission_classes([AllowAny])
def kakao_callback(request, format=None):
    kakao_rest_api_key = env('kakao_rest_api_key')
    kakao_redirect_uri = env('kakao_redirect_uri')

    code = request.GET.get('code', None)
    headers = {
        'Access-Control-Allow-Origin': 'https://www.myplanit.site',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }
    data = {
        'grant_type': 'authorization_code',
        'client_id': kakao_rest_api_key,
        'redirect_uri': kakao_redirect_uri,
        'code': code
    }

    url = 'https://kauth.kakao.com/oauth/token'

    token_req = requests.post(url, headers=headers, data=data)
    token_req_json = token_req.json()
    access_token = token_req_json.get("access_token")
    refresh_token = token_req_json.get("refresh_token")
    print("access_token: ", access_token)
    print("refresh_token: ", refresh_token)

    kakao_api_response = requests.post(
        "https://kapi.kakao.com/v2/user/me",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "Access-Control-Allow-Origin": "https://www.myplanit.site",
        },
    )
    kakao_api_response = kakao_api_response.json()
    user_id = kakao_api_response.get('id')
    # if user_id is None:
    #    return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)
    username = f'user{user_id}'

    realname = kakao_api_response.get('properties').get('nickname')
    print(username, realname)

    # 추가
    # requests.post("https://kapi.kakao.com/v1/user/unlink",
    #               headers={"Authorization": f"Bearer {access_token}"},
    #               )

    try:
        user = User.objects.get(username=username)
        print("기존 유저")

    except:
        user = User(username=username, realname=realname)
        user = user.save()
        user = User.objects.get(username=username)
        print("새로운 유저")

    data = {'username': username, 'django_token': get_tokens_for_user(user), 'kakao_accessToken': access_token}
    print(data)
    return Response(data, status=200)


# 관리자 로그인 - 프론트 개발용
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request, format=None):
    try:
        username = request.data['username']
        password = request.data['password']
        user = User.objects.get(username=username)
        if check_password(password, user.password):
            user = authenticate(username=username, password=password)
            data = {'username': username, 'django_token': get_tokens_for_user(user)}
            return Response(data, status=200)
    except:
        return Response({"message": "error"}, status=status.HTTP_400_BAD_REQUEST)


# 로그아웃 -> 사용자의 access_token, refresh_token 모두 만료시킴
def kakao_logout(request):
    access = "2zqeoqTJQ-u-a1SiB1ga2SnPv2LIX8OiSQ5oego9cxgAAAF_LK3m6g"
    data = requests.post(
        "https://kapi.kakao.com/v1/user/logout",
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