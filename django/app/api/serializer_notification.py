# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

