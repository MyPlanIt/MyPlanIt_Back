from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from .serializers import SignupSerializer

# Create your views here.


# 회원가입
class SignupView(APIView):
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = SignupSerializer(data=data)

        if serializer.is_valid():
            try:
                user = serializer.save()
            except:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # jwt token
            token = TokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            response = Response(
                {
                    "user": serializer.data,
                    "message": "success registered",
                    "token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                },
                status = status.HTTP_200_OK
            )
            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)