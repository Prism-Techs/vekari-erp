from django.shortcuts import render
from .models import Notification
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from .serializers import NotificationSerializer,NotificationReadSerializer
# Create your views here.
class NotificationAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    def get_queryset(self):
        is_read = self.request.query_params.get('is_read')
        if is_read:
            return Notification.objects.filter(receiver_user=self.request.user.id,is_read=is_read).order_by('-created_date')

        return Notification.objects.filter(receiver_user=self.request.user.id,is_read=0).order_by('-created_date')

class NotificationRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    # queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    def get_queryset(self):
        is_read = self.request.query_params.get('is_read')
        if is_read:
            return Notification.objects.filter(receiver_user=self.request.user.id,is_read=is_read).order_by('-created_date')

        return Notification.objects.filter(receiver_user=self.request.user.id,is_read=0).order_by('-created_date')
    
class NotificationReadAPIView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    serializer_class = NotificationReadSerializer