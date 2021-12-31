from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings

from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'realname', 'phone_num', 'nickname']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        realname = validated_data.get('realname')
        phone_num = validated_data.get('phone_num')
        nickname = validated_data.get('nickname')
        user = User(
            email = email,
            realname = realname,
            phone_num = phone_num,
            nickname = nickname
        )
        user.set_password(password)
        user.save()
        return user
