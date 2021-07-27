from django.contrib import admin

# Register your models here.
from .models import User, Brand, Event, Category, SubscribeBrand, SubscribeEvent, Notification

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(SubscribeBrand)
admin.site.register(SubscribeEvent)
admin.site.register(Notification)