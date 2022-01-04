from rest_framework import serializers, fields
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.settings import api_settings
from .models import JOB_CHOICES

from .models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'realname', 'phone_num', 'username']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        realname = validated_data.get('realname')
        phone_num = validated_data.get('phone_num')
        username = validated_data.get('username')
        user = User(
            email = email,
            realname = realname,
            phone_num = phone_num,
            username = username
        )
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'realname', 'username']


class OnbordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['jobs']