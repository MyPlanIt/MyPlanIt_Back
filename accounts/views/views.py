from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import update_last_login

User = get_user_model()


# 기존
# 회원가입
class SignupView(APIView):
    permission_classes = (AllowAny,)

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

            # payload = JWT_PAYLOAD_HANDLER(user)
            # jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            # data = {'token': jwt_token}
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
