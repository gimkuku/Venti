# coding=utf-8
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser

from .models import SubscribeBrand
from .serializer_subscribeBrand import SubscribeBrandSerializer
from django_filters.rest_framework import FilterSet, filters
from django_filters.rest_framework import DjangoFilterBackend

# 브랜드 좋아요 버튼, 마이브랜드_브랜드


class SubscribeBrandFilter(FilterSet):
    user = filters.NumberFilter(field_name="user")

    class Meta:
        model = SubscribeBrand
        fields = ['user']


class SubscribeBrandViewSet(viewsets.ModelViewSet):
    """
        유저의 브랜드 구독 목록을 불러오거나 저장/삭제 하는 API
        ---
        # 예시
            - GET /api/mybrands/
            - POST /api/mybrands/
            - POST /api/mybrands/users/
            - DELETE /api/mybrands/{id}
    """
    serializer_class = SubscribeBrandSerializer
    queryset = SubscribeBrand.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SubscribeBrandFilter

    @action(detail=False, methods=['post'])
    def users(self, request):
        data = JSONParser().parse(request)
        user = data['user']
        my = SubscribeBrand.objects.filter(user=user)
        mybrand = my.values()
        return JsonResponse({'mybrand': list(mybrand)}, status=200)