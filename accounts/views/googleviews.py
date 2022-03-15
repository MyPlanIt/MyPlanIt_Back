from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
import requests

from accounts.views.kakaoviews import get_tokens_for_user
from myplanit.settings.base import env

User = get_user_model()

# 전역 변수로 설정
client_id = env('GOOGLE_CLIENT_ID')
redirect_uri = "http://localhost:3000/auth/google/callback"
scope = "https://www.googleapis.com/auth/userinfo.profile"
client_secret = env('GOOGLE_CLIENT_SECRET')


# 인증 코드 요청
@api_view(['GET'])
@permission_classes([AllowAny])
def get_code(request):
    google_login_endpoint = "https://accounts.google.com/o/oauth2/v2/auth"
    code_redirect_uri = 'https://myplanit.link/login/google/callback'
    return redirect(
        f"{google_login_endpoint}?client_id={client_id}&redirect_uri={code_redirect_uri}&response_type=code&scope={scope}"
    )


# 구글 회원가입 & 로그인
@api_view(['GET'])
@permission_classes([AllowAny])
def google_callback(request, format=None):
    # 인증 코드로 구글 제공 access token 발급
    google_get_token_endpoint = 'https://oauth2.googleapis.com/token'
    auth_code = request.GET.get('code', None)

    # 인증 코드 decode 과정
    if '%' in auth_code:
        auth_code = auth_code.replace('%2F', '/')

    headers = {
        'Access-Control-Allow-Origin': 'http://localhost:3000',
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8',
    }

    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': redirect_uri,
    }

    token_req = requests.post(google_get_token_endpoint, headers=headers, data=data)
    if not token_req.ok:
        raise ValidationError('Invalid token')

    token_req_json = token_req.json()

    access_token = token_req_json.get("access_token")
    print("access_token: ", access_token)

    user_info_json = requests.get(
        "https://www.googleapis.com/oauth2/v3/userinfo",
        params={
            'access_token': access_token
        },
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            "Access-Control-Allow-Origin": "http://localhost:3000"
        }
    )

    if not user_info_json.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    user_info = user_info_json.json()
    username = user_info.get('sub')
    realname = user_info.get('family_name') + user_info.get('given_name')

    exist_user_flag = User.objects.filter(username=username)

    if exist_user_flag.exists():
        print("기존 유저")

    else:
        print("신규 유저")
        user = User(username=username, realname=realname)
        user = user.save()

    user = User.objects.get(username=username)
    print(user)

    data = {
        'username': username,
        'realname': realname,
        'django_token': get_tokens_for_user(user)
    }

    print(data)
    return Response(data, status=status.HTTP_200_OK)
