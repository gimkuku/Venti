from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import SubscribeEvent


class SubscribeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribeEvent
        fields = '__all__'
