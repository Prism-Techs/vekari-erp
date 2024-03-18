import json
from django.http import HttpRequest
from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date
from django.utils import timezone
from .models import *
import os
from authuser.models import AuthUser
from django.db.models import Q, F
from django.db.models import Max

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
    
    def to_representation(self, instance:Notification):
        data=super().to_representation(instance)

       
        sender=AuthUser.objects.get(id=instance.sender_user_id)
        data['receiver_username']=instance.receiver_user.username
        data['receiver_fname']=instance.receiver_user.first_name
        data['receiver_lname']=instance.receiver_user.last_name
        data['sender_username']=sender.username
        data['sender_fname']=sender.first_name
        data['sender_lname']=sender.last_name
        return data
    def update(self, instance, validated_data):
        
        return super().update(instance, validated_data)
class NotificationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['is_read']
    
    def to_representation(self, instance:Notification):
        data=super().to_representation(instance)

       
        sender=AuthUser.objects.get(id=instance.sender_user_id)
        data['receiver_username']=instance.receiver_user.username
        data['receiver_fname']=instance.receiver_user.first_name
        data['receiver_lname']=instance.receiver_user.last_name
        data['sender_username']=sender.username
        data['sender_fname']=sender.first_name
        data['sender_lname']=sender.last_name
        return data
    def update(self, instance, validated_data):

        return super().update(instance, validated_data)