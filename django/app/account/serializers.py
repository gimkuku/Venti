# coding=utf-8
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_auth.registration.serializers import RegisterSerializer
from api.models import User
from .models import *

# JWT 사용을 위한 설정
JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

# 사용자 정보 추출
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

# # 기본 유저 모델 불러오기
User = get_user_model()

# 회원가입
class CustomRegisterSerializer(RegisterSerializer):
    nickname = serializers.CharField(required=False, max_length=50)
    gender = serializers.CharField(required=False, max_length=50)
    birth = serializers.DateField(required=False)

    def __init__(self,*args,**kwargs):
        super(CustomRegisterSerializer,self).__init__(*args,**kwargs)

    def get_cleaned_data(self):
        data_dict = super(CustomRegisterSerializer,self).get_cleaned_data() # username, password, email이 디폴트
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['birth'] = self.validated_data.get('birth', '')

        return data_dict



# 로그인
class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password", None)
        # 사용자 아이디와 비밀번호로 로그인 구현(<-> 사용자 아이디 대신 이메일로도 가능)
        user = authenticate(username=username, password=password)

        if user is None:
            return {'username': 'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given username and password does not exist'
            )
        return {
            'username': user.username,
            'token': jwt_token
        }

# 회원수정
class UpdateSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'birth', 'gender', 'email']


# 회원탈퇴
class UnsubscribeSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['username']
