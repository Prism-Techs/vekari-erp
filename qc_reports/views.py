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
from .filters.qcr_filter import QC_ReportFilter
from .models import *



class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"



class QCReport_APIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=QcReportsMaster.objects.all()   
    serializer_class = QCReportSerializer
    group_permissions = ['quality']   
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = QC_ReportFilter
    ordering_fields = ['created_date','part__product_part_no','status','vendor__vendor_name']
    ordering=['-created_date']
   
class QCReportRetrieve_APIView(generics.RetrieveUpdateDestroyAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=QcReportsMaster.objects.all()   
    serializer_class = QCReportSerializer
    group_permissions = ['quality']   
  
# class QC_search_APIView(generics.ListAPIView,):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated,YourPermission]
#     queryset=QcMaster.objects.all()
#     serializer_class = QC_Serializer
#     group_permissions = ['settings']   
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['part__part_id',]
#     ordering_fields = ['created_date',]
#     ordering = ['-created_date']
# class QC_RetrieveAPIView(generics.RetrieveUpdateDestroyAPIView,):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated,YourPermission]
#     queryset=QcMaster.objects.all()
#     serializer_class = QC_Serializer
#     group_permissions = ['settings']   
#     filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['created_date__date','part__product_part_no','product_part_no__product_part_name']
#     ordering_fields = ['created_date',]
#     ordering = ['-created_date']

#     def destroy(self, request, *args, **kwargs):
#         id=kwargs.get('pk')
#         if QcMaster.objects.filter(qc_id=id).exists():
#             QcMaster.objects.filter(qc_id=id).update(is_remove=True)
#             return Response(status=status.HTTP_200_OK,data={"message":"succussfully deleted."})
#         return Response(status=status.HTTP_204_NO_CONTENT,)