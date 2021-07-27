# coding=utf-8
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Event
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

response_schema_dict = {
    "200": openapi.Response(
        description="인기 많은 이벤트 보여줌",
        examples={
            "application/json": {
                "result": [
                    {
                        "id": 1,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-11",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "vips_Event1",
                        "image": "",
                        "banner_image": "",
                        "text": "v",
                        "due": "2021-07-21",
                        "weekly_view": 4,
                        "url": "www.naver.com"
                    },
                    {
                        "id": 2,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-11",
                        "category_id": 1,
                        "brand_id": 1,
                        "name": "vips_Event2",
                        "image": "",
                        "banner_image": "",
                        "text": "vv",
                        "due": "2021-07-21",
                        "weekly_view": 3,
                        "url": "www.naver.com"
                    },
                    {
                        "id": 3,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-11",
                        "category_id": 2,
                        "brand_id": 3,
                        "name": "star_Event1",
                        "image": "",
                        "banner_image": "",
                        "text": "s1",
                        "due": "2021-07-21",
                        "weekly_view": 2,
                        "url": "www.naver.com"
                    },
                    {
                        "id": 4,
                        "created_date": "2021-07-11",
                        "update_date": "2021-07-11",
                        "category_id": 3,
                        "brand_id": 4,
                        "name": "nike_Event1",
                        "image": "",
                        "banner_image": "",
                        "text": "n1",
                        "due": "2021-07-21",
                        "weekly_view": 1,
                        "url": "www.naver.com"
                    }
                ]
            }
        }
    )
}



class Weekly(APIView):
    """
        인기 이벤트를 불러오거나 저장/수정/삭제 하는 API
        ---
        # 예시
            - GET /api/weekly/
        # parameters
            - No parameters
        # Responses
            - result : [인기 이벤트 목록]
    """

    def get(self, request, format=None):
        hot_event = Event.objects.all().order_by('-weekly_view')
        result = hot_event.values()
        return JsonResponse({'result': list(result)}, status=200)
