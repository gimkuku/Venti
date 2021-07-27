# coding=utf-8
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .serializer_event import EventSerializer
from .models import Brand

# 수정필요
class SearchSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'image', 'events']
