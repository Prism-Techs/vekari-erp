from rest_framework import filters  
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from authuser.permission import YourPermission 
from .serializers import *
from .models import *
# Create your views here.

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class QC_APIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=QcMaster.objects.all()
    serializer_class = QC_Serializer
    group_permissions = ['quality']   
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['part__part_id','part__product_part_name']
    ordering_fields = ['created_date',]
    ordering = ['-created_date']
class tools_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=ToolsMaster.objects.all()
    serializer_class = ToolsSerailizer
    group_permissions = ['quality','settings']   
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tool_name','created_date__date']
    ordering_fields = ['created_date','tool_name']
    ordering = ['-created_date']
    lookup_field='slug'
class tools_RetrieveAPIView(generics.RetrieveAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=ToolsMaster.objects.all()
    serializer_class = ToolsSerailizer
    group_permissions = ['quality','settings']  
    lookup_field='slug'

    def destroy(self, request, *args, **kwargs):
        slug=kwargs.get('slug')
        if ToolsMaster.objects.filter(slug=slug).exists():
            ToolsMaster.objects.filter(slug=slug).update(is_remove=True)
            return Response(status=status.HTTP_200_OK,data={"message":"succussfully deleted."})
        return Response(status=status.HTTP_204_NO_CONTENT,)
    
    
class Alltools_APIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=ToolsMaster.allobjects.all()
    serializer_class = ToolsSerailizer
    group_permissions = ['settings']   
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['tool_name','created_date__date']
    ordering_fields = ['created_date','tool_name']
    ordering = ['-created_date']
    # lookup_field='slug'

class Alltools_RetrieveAPIView(generics.RetrieveUpdateDestroyAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=ToolsMaster.allobjects.all()
    serializer_class = ToolsSerailizer
    group_permissions = ['settings']   
    # lookup_field='slug'

    def destroy(self, request, *args, **kwargs):
        slug=kwargs.get('slug')
        if ToolsMaster.allobjects.filter(slug=slug).exists():
            ToolsMaster.allobjects.filter(slug=slug).update(is_remove=True)
            return Response(status=status.HTTP_200_OK,data={"message":"succussfully deleted."})
        return Response(status=status.HTTP_204_NO_CONTENT,)

class QC_search_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=QcMaster.objects.all()
    serializer_class = QC_Serializer
    group_permissions = ['quality']   
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['part__part_id',]
    ordering_fields = ['created_date',]
    ordering = ['-created_date']
class QC_RetrieveAPIView(generics.RetrieveUpdateDestroyAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=QcMaster.objects.all()
    serializer_class = QC_Serializer
    group_permissions = ['quality']   
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['created_date__date','part__product_part_no','product_part_no__product_part_name']
    ordering_fields = ['created_date',]
    ordering = ['-created_date']

    def destroy(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        if QcMaster.objects.filter(qc_id=id).exists():
            QcMaster.objects.filter(qc_id=id).update(is_remove=True)
            return Response(status=status.HTTP_200_OK,data={"message":"succussfully deleted."})
        return Response(status=status.HTTP_204_NO_CONTENT,)

class Inspection_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=InspectionTypeMaster.objects.all()
    serializer_class=InspectionSerailizer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['inspt_name']
    ordering_fields = ['inspt_name',]
    ordering = ['-inspt_name']
class PartBoughtOut_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    queryset=PartsMaster.objects.filter(product_type=1,source__s_name='Bought-out')
    serializer_class=PartBoughtOutSerailizer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['product_part_no','product_part_name','product_descp']
    ordering_fields = ['product_part_no','product_part_name','product_descp']
    ordering = ['-product_part_no']
