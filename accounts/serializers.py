from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings

# JWT 사용을 위한 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'realname', 'username', 'email_agree', 'sns_agree']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        realname = validated_data.get('realname')
        username = validated_data.get('username')
        email_agree = validated_data.get('email_agree')
        sns_agree = validated_data.get('sns_agree')

        if User.objects.filter(email=email).exists():
            return serializers.ValidationError("email이 이미 존재합니다.")
        if User.objects.filter(username=username).exists():
            return serializers.ValidationError("nickname이 이미 존재합니다.")

        user = User(
            email=email,
            realname=realname,
            username=username,
            email_agree=email_agree,
            sns_agree=sns_agree
        )
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user_email = authenticate(email=email, password=password)
        user = User.objects.get(email=user_email)

        payload = JWT_PAYLOAD_HANDLER(user)
        jwt_token = JWT_ENCODE_HANDLER(payload)
        update_last_login(None, user)

        return {
            'username': user.username,
            'token': jwt_token
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'realname', 'username']


class OnbordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['jobs']


class UserProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'realname']