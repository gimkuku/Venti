# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from .models import Event, Brand
from .serializer_search import SearchSerializer
from .serializer_brand import BrandSerializer
from .serializer_event import EventSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend


class BrandFilter(APIView):
    """
        브랜드 필터링을 거친 이벤트 목록을 불러오는 API ( 삭제예정 )
        ---
        # 예시
            - POST /api/brandfilter/
        # parameter
            - event_list:[필터링 이벤트 목록]
    """

    def post(self, request, format=None):
        data = JSONParser().parse(request)
        arr = []
        category = data['category']
        for i in data['brand']:
            result_set = Event.objects.filter(brand=i, category=category)
            if len(list(result_set)) != 0:
                arr.append(list(result_set.values()))

        return JsonResponse({'event_list': arr}, status=200)

    def get(self, request):
        return HttpResponse(status=200)
