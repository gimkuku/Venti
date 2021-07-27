# coding=utf-8
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Event, Notification
from .serializer_notification import NotificationSerializer
from django.views.decorators.csrf import csrf_exempt
from background_task import background
from .models import *
from rest_framework.decorators import authentication_classes, permission_classes
from datetime import datetime, timedelta

class Notifications(APIView):
    """
        알림을 저장 하는 API ( 마감 알림 요청 )
        ---
        # 예시
            - POST /api/notifications/
        # parameters
            - "user" : 1 (유저 id)
            - "notice_type" : "end" (고정)
            - "event" : 1 (이벤트 id)
            - "url" : "www.naver.com" (이벤트 url) - NULL 가능
        # Responses
            - "user":
            - "notice_type":
            - "event":
            - "brand":
            - "url":
    """
    # 이거는 프엔에서 마감시간때 post 해서 알람디비 채워주는건데 안될것같으면 지워도 될듯
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class NotificationUser(APIView):
    """
        특정 유저의 알림을 불러오는 API
        ---
        # 예시
            - POST /api/notifications/users/
        # parameters
            - "users" : 1 (유저 id)
        # Responses
            - result : [알림 목록]
    """
    def post(self, request, format=None):
        data = JSONParser().parse(request)
        user = data['user']
        noti = Notification.objects.filter(user=user).order_by('-id')[:30]   # 30개까지 최신순 정렬
        result = noti.values()
        return JsonResponse({'result': list(result)}, status=200)


@permission_classes([])
@authentication_classes([])
def noti(request):
    if request.method == "POST":
        noti_bg(repeat=120)
        return JsonResponse({"success":"true"}, status=302)
    return JsonResponse({}, status=404)

@background(schedule=120)
def noti_bg():
    # 현재 시간 가져오기
    now = datetime.now().strftime('%Y-%m-%d %h:%m:%s')
    # 12시간 전
    now12 = datetime.now() + timedelta(hours=12)
    now24 = datetime.now() + timedelta(hours=24)
    now48 = datetime.now() + timedelta(hours=48)
    # 12시간 전 이벤트들
    endevent12 = Event.objects.filter(due__gte=(now12 - timedelta(minutes=1)),due__lte=(now12 + timedelta(minutes=1)))
    endevent24 = Event.objects.filter(due__gte=(now24 - timedelta(minutes=1)), due__lte=(now24 + timedelta(minutes=1)))
    endevent48 = Event.objects.filter(due__gte=(now48 - timedelta(minutes=1)), due__lte=(now48 + timedelta(minutes=1)))

    # 이 이벤트를 좋아하는 유저 찾기
    if endevent12.count() != 0:
        for i in endevent12:
            likeevents = SubscribeEvent.objects.filter(event = i.id)
            for j in likeevents:
                Notification.objects.create(user=j.user, event= i, brand=i.brand, notice_type="end")
    # 이 이벤트를 좋아하는 유저 찾기
    if endevent24.count() != 0:
        for i in endevent24:
            likeevents = SubscribeEvent.objects.filter(event = i.id)
            for j in likeevents:
                Notification.objects.create(user=j.user, event= i, brand=i.brand, notice_type="end")
    # 이 이벤트를 좋아하는 유저 찾기
    if endevent48.count() != 0:
        for i in endevent48:
            likeevents = SubscribeEvent.objects.filter(event = i.id)
            for j in likeevents:
                Notification.objects.create(user=j.user, event= i, brand=i.brand, notice_type="end")