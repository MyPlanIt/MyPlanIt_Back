import jwt.exceptions
import rest_framework_simplejwt.exceptions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse

from myplanit.settings import env
from .models import User
from .serializers import SignupSerializer, UserSerializer
import jwt
from jwt_token.jwt_token import get_token, get_user


# 회원가입
class SignupView(APIView):
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

            # 회원가입 이후 첫 토큰 발행
            token = TokenObtainPairSerializer.get_token(user)  # refresh 토큰 가져오기
            refresh_token = str(token)
            access_token = str(token.access_token)  # access 토큰 가져오기
            response = Response({"message": "회원가입 완료"}, status=status.HTTP_201_CREATED)
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)
            return response

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)



# 로그인
class LoginView(APIView):
    # 토큰으로 유저 정보 조회
    def get(self, request):
        try:
            access_token = request.COOKIES['access_token']
            payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
            pk = payload.get('user_id')
            user = get_user(pk)
            serializer = UserSerializer(user)
            response = Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', request.COOKIES['refresh_token'])
            return response

        # 토큰 만료시 토큰 갱신
        except(jwt.exceptions.ExpiredSignatureError):
            try:
                print("access만료")
                serializer = TokenRefreshSerializer(data={'refresh': request.COOKIES.get('refresh_token', None)})

                if serializer.is_valid(raise_exception=True):
                    access_token = serializer.validated_data['access']
                    refresh_token = request.COOKIES.get('refresh_token', None)
                    payload = jwt.decode(access_token, env('DJANGO_SECRET_KEY'), algorithms=['HS256'])
                    pk = payload.get('user_id')
                    user = get_user(pk)
                    serializer = UserSerializer(instance=user)
                    response = Response(serializer.data, status=status.HTTP_200_OK)
                    response.set_cookie('access_token', access_token)
                    response.set_cookie('refresh_token', refresh_token)
                    return response
            except(rest_framework_simplejwt.exceptions.TokenError):
                print("refresh토큰도 만료")
                return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

            raise jwt.exceptions.InvalidTokenError

        except(jwt.exceptions.InvalidTokenError):
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)

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
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_401_UNAUTHORIZED
            )

        if user is not None: # 모두 성공 시
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": UserSerializer(user).data,
                    "message": "login success",
                    "jwt_token": {
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
                data={"message": "로그인에 실패하였습니다"}, status=status.HTTP_404_NOT_FOUND
            )


# 온보딩
class OnboardingView(APIView):
    def post(self, request):
        jobs = request.data.get('jobs')
        interests = request.data.get('interests')

        try:
            res = list(get_token(request))  # 토큰 함수 호출 -> user, access, refresh 토큰 반환함
            user = res[0]
            access_token = res[1]
            refresh_token = res[2]
            response = Response(data={"message": "success"}, status=status.HTTP_200_OK)
            response.set_cookie('access_token', access_token)
            response.set_cookie('refresh_token', refresh_token)

            user.jobs = jobs
            user.interests = interests
            user.save()
            return response

        except: # get_token 함수가 None 반환 시
            return Response({"message": "로그인이 만료되었습니다."}, status=status.HTTP_400_BAD_REQUEST)