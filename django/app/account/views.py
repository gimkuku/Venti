
# coding=utf-8
from rest_framework import status, mixins

# FBV
from rest_framework.response import Response

from rest_framework import generics  # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from django.contrib.auth.decorators import login_required

# JWT 사용을 위해 필요
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from typing import Dict, Any

from .serializers import *
from .models import *
from .forms import *

from rest_framework.views import APIView
#redoc
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

register_response_schema_dict = {
    "201": openapi.Response(
        description="새로운 회원 추가 완료",
        examples={
            "application/json":
                {"user": {"id": 10, "username": "kuku.."}}
        }
    ),
    "400": openapi.Response(
        description="회원 가입 실패",
        examples={
            "application/json":
                {"username":["해당 사용자 이름은 이미 존재합니다."],"email":["이미 이 이메일 주소로 등록된 사용자가 있습니다."]}
        }
    ),
}

login_response_schema_dict = {
    "200": openapi.Response(
        description="로그인 성공",
        examples={
            "application/json": {
                "token": "eyJ0eXAiOiJK어쩌구"
            }
        }
    ),
    # "401": openapi.Response(
    #         description="만료된 토큰 ",
    #         examples={
    #             "application/json": {
    #                     "detail": "Signature has expired."
    #                 }
    #         }
    #     ),
    "401": openapi.Response(
            description="로그인 실패 ",
            examples={
                "application/json": {
                        "message": "fail"
                    }
            }
        )
}

update_response_schema_dict = {
    "200": openapi.Response(
        description="회원 수정 성공",
        examples={
            "application/json":     {
                    "name": "kuku"
                }
        }
    )
}

unsubscribe_response_schema_dict= {
    "201": openapi.Response(
        description="탈퇴 성공",
        examples={
            "application/json":     {
                    "success": True,
                }
        }
    )
}

# 회원가입
@permission_classes([AllowAny])
class Registration(generics.GenericAPIView):
    """
        회원가입
        ---
        # URL
            - POST /accounts/create/
        # 전달 형식 : formdata
            - { username : string,
                password1 : string, //비밀번호
                password2 : string, //확인용 다시치는 비밀번호
                nickname : string,
                email : string,
                gender : string,
                birth : date,
                }
     """

    serializer_class = CustomRegisterSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='id'),
                'password1': openapi.Schema(type=openapi.TYPE_STRING, description='pwd'),
                'password2': openapi.Schema(type=openapi.TYPE_STRING, description='확인용 다시 친 pwd'),
                'nickname': openapi.Schema(type=openapi.TYPE_STRING, description='닉네임'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='이메일 '),
                'gender': openapi.Schema(type=openapi.TYPE_STRING, description='성별'),
                'birth': openapi.Schema(type=openapi.TYPE_STRING, description='생일'),
            }
        ),
        responses = register_response_schema_dict)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)  # request 필요 -> 오류 발생
        return Response(
            {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data
            },
            status=status.HTTP_201_CREATED,
        )


# 회원 정보 수정
class Update(generics.GenericAPIView):
    """
        회원 수정
        ---
        # URL
            - POST /accounts/update/
        # header
            - Authorization : JWT ey93... [jwt token]
        # 전달 형식 : formdata
            - {
                nickname : string, //변경된 사항만 보내주면 됨! default로 설정해놓고 다 보내도 상관 음슴!
                email : string,
                gender : string,
                birth : date,
                }
     """

    serializer_class = UpdateSerializer
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'nickname':openapi.Schema(type=openapi.TYPE_STRING, description='닉네임'),
                'email' : openapi.Schema(type=openapi.TYPE_STRING, description='이메일 '),
                'gender' : openapi.Schema(type=openapi.TYPE_STRING, description='성별'),
                'birth' : openapi.Schema(type=openapi.TYPE_STRING, description='yyyy-mm-dd 생일'),
            }
        ),
        responses=update_response_schema_dict)
    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        user = request.user
        if request.POST.get('birth'):
            user.birth = request.POST["birth"]
        if request.POST.get('gender'):
            user.gender = request.POST["gender"]
        if request.POST.get('nickname'):
            user.nickname = request.POST["nickname"]
        if request.POST.get('email'):
            user.email = request.POST["email"]
        user.save()
        # if not form.is_valid():
        #     return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        return Response(
            {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                "name": user.username,
            },
            status=status.HTTP_201_CREATED,
        )

#로그인
@permission_classes([AllowAny])
class Login(generics.GenericAPIView):
    """
        회원 로그인

        # URL
            - POST /accounts/login/

        # 전달 형식 : formdata
            - {
                username : string   // id
                password : string   // pwd
               }
    """
    serializer_class = UserLoginSerializer
    @swagger_auto_schema(request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username':openapi.Schema(type=openapi.TYPE_STRING, description='id'),
                'password' : openapi.Schema(type=openapi.TYPE_STRING, description='pwd'),
            }
        ),responses=login_response_schema_dict)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        if user['username'] == "None":
            return Response({"message": "fail"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(
            {
                "token": user['token']
            }
        )


# 회원 탈퇴
@permission_classes([IsAuthenticated])
class Unsubscribe(generics.GenericAPIView):
    """
        회원 탈퇴
        ---
        # URL
            - POST /accounts/unsubscribe/
        # header
            - Authorization : JWT ey93... [jwt token]
        # 전달 형식 : formdata
            - {
                username : string   //본인확인용
               }
     """
    serializer_class = UnsubscribeSerializer
    @swagger_auto_schema(request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username':openapi.Schema(type=openapi.TYPE_STRING, description='id (탈퇴 확인 같은거.. 한번 치라고)'),
            }
        ),responses=unsubscribe_response_schema_dict)
    def post(self, request, *args, **kwargs):
        # serializer = self.get_serializer(data=request.data)
        user = request.user
        if user.username == request.POST["username"]:
            user.delete()
            return Response(
                {
                    "success": True,
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {
                    "success": False,
                    "user" : user.username,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )



