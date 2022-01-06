from rest_framework import serializers
from .models import User


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'realname', 'phone_num', 'username', 'email_agree', 'sns_agree']

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        realname = validated_data.get('realname')
        phone_num = validated_data.get('phone_num')
        username = validated_data.get('username')
        email_agree = validated_data.get('email_agree')
        sns_agree = validated_data.get('sns_agree')

        if User.objects.filter(email=email).exists():
            return serializers.ValidationError("email이 이미 존재합니다.")
        if User.objects.filter(username=username).exists():
            return serializers.ValidationError("nickname이 이미 존재합니다.")

        user = User(
            email = email,
            realname = realname,
            phone_num = phone_num,
            username = username,
            email_agree = email_agree,
            sns_agree = sns_agree
        )
        user.set_password(password)
        user.save()
        return user


class UserSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'realname', 'username']


class OnbordingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['jobs']