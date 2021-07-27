# coding=utf-8
# from rest_framework import viewsets
import json
# from rest_framework_swagger import renderers
# from rest_framework.decorators import api_view, renderer_classes
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .models import Event, SubscribeBrand
from django.http import JsonResponse, HttpResponse
from .serializer_subscribeBrand import UseridSerializer
from rest_framework.parsers import JSONParser
# from api.utils import error_collections

#redoc
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# eventforyou
# @renderer_classes([renderers.OpenAPIRenderer, renderers.SwaggerUIRenderer])
from drf_yasg.inspectors import SwaggerAutoSchema
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

response_schema_dict = {
    "200": openapi.Response(
        description="사용자가 좋아요 한 브랜드의 이벤트를 보여준다.",
        examples={
            "application/json": {
                    "eventforyou": [
                        {
                            "id": 4,
                            "created_date": "2021-07-10",
                            "update_date": "2021-07-10",
                            "category_id": 2,
                            "brand_id": 6,
                            "name": "투썸케잌신메뉴",
                            "image": "스크린샷_2021-07-10_오후_9.19.23.png",
                            "banner_image": "스크린샷_2021-07-09_오후_7.40.17.png",
                            "text": "투썸케잌신메뉴투썸케잌신메뉴투썸케잌신메뉴",
                            "due": "2021-07-17",
                            "weekly_view": 1,
                            "url": "https://www.nike.com/kr/ko_kr/c/nike-membership"
                        },
                        {
                            "id": 6,
                            "created_date": "2021-07-10",
                            "update_date": "2021-07-10",
                            "category_id": 2,
                            "brand_id": 6,
                            "name": "투썸 이제 한국꺼아님",
                            "image": "스크린샷_2021-07-08_오후_6.28.09.png",
                            "banner_image": "스크린샷_2021-07-08_오후_6.33.22_NF4N80g.png",
                            "text": "홍콩껀가?그래",
                            "due": "2021-07-18",
                            "weekly_view": 1,
                            "url": "https://www.nike.com/kr/ko_kr/c/nike-membership"
                        },
                        {
                            "id": 9,
                            "created_date": "2021-07-10",
                            "update_date": "2021-07-10",
                            "category_id": 1,
                            "brand_id": 1,
                            "name": "나이키온마슈즈~",
                            "image": "스크린샷_2021-07-10_오후_9.18.56_2uqKi2h.png",
                            "banner_image": "스크린샷_2021-07-09_오후_7.40.17_ftMHPKi.png",
                            "text": "멕미 펄펙",
                            "due": "2021-07-10",
                            "weekly_view": 1,
                            "url": "https://www.nike.com/kr/ko_kr/c/nike-membership"
                        }
                    ]
            }
        }
    )
}

@permission_classes([])
@authentication_classes([JSONWebTokenAuthentication,])
class EventforyouView(APIView):
    """
        메인페이지의 EventForYou 이벤트 목록을 불러오는 API
        ---
        # 예시
            - POST /api/eventforyou/
        # parameter
            - {user : 1} : user 의 id 를 JSON형식으로 전달

     """
    model = Event, SubscribeBrand
    # post : post 로 날라온 유저의 eventforyou 찾아주기

    @swagger_auto_schema(request_body= openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'user': openapi.Schema(type=openapi.TYPE_NUMBER, description='int'),
        }
    ), responses=response_schema_dict)
    def post(self, request):
        events = []
        user = request.POST['user']
        subscribebrands = SubscribeBrand.objects.filter(user=user)
        for i in subscribebrands :
            eventforyou = Event.objects.filter(brand=i.brand)
            for j in eventforyou.values() :
                events.append(j)
        return JsonResponse({'eventforyou' : events}, status=200)
