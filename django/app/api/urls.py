# coding=utf-8
from django.urls import path, include
from api import views
from .views import UserViewSet
from rest_framework.routers import DefaultRouter
# 기능 구현하고 import ( 밑에 router 연결도 해야함 )
# 현진
# from .view_login import ~ViewSet
# .view_join import ~ViewSet
# .view_mainpage import ~ViewSet
# 준기
from . import view_notification
from .view_brand import BrandViewSet
from .view_event import EventViewSet
from .view_subscribeEvent import SubscribeEventViewSet
from .view_subscribeBrand import SubscribeBrandViewSet
from .views_search import Search
from .view_eventforyou import EventforyouView
from .view_weekly import Weekly
from .view_notification import *
# 추가
# .view_notification import ~ViewSet
# 관리자 기능? 관련

# CBV
# urlpatterns = [
#     path('post/', views.PostList.as_view()),
#     path('post/<int:pk>', views.PostDetail.as_view())
#     ]

# ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'events', EventViewSet)
# router.register(r'eventforyou', EventForYouViewSet)
router.register(r'myevents', SubscribeEventViewSet)
router.register(r'mybrands', SubscribeBrandViewSet)
# router.register(r'search', Search)    # post 용도로만

urlpatterns = [
    path('', include(router.urls)),
    path('notifications/', Notifications.as_view()),
    path('notifications/users/', NotificationUser.as_view()),
    path('noti/', view_notification.noti),
    path('search/', Search.as_view()),
    path('weekly/', Weekly.as_view()),
    path('eventforyou/', EventforyouView.as_view(),name = "eventforyou"),
]