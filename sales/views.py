from django.shortcuts import render
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from .serializers import MatchineDispatchSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters  
from .models import *


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"

class MachineDispatchAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DespatchMaster.objects.all()
    serializer_class = MatchineDispatchSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['cmodel','ccity','cextype','cnam','cmachineno','ddespatcdt']

class MachineDispatchRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = DespatchMaster.objects.all()
    serializer_class = MatchineDispatchSerializer
    lookup_field='nno'

    def perform_destroy(self, instance):
        # Instead of actually deleting the instance, update is_delete to 0
        instance.is_delete = 0
        instance.status = 0
        instance.save()