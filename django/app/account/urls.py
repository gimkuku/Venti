# urls.py (app)
from django.urls import path
from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

from . import views

urlpatterns = [
    # token
    path('token/refresh/', refresh_jwt_token),
    path('create/', views.Registration.as_view()),
    path('login/', views.Login.as_view()),
    path('update/', views.Update.as_view()),
    path('unsubscribe/', views.Unsubscribe.as_view()),
]