from django.shortcuts import render
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
from authuser.models import UserApproval

# Create your views here.
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class PR_APIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=PrProcessMaster.objects.all()
    serializer_class = PR_ProcessSerializer
    group_permissions = ['supply_chain']   
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['created_date__date','status','prp_id','prp_no']
    # Specify the fields by which the client can order the results
    ordering_fields = ['created_date','status','prp_id','prp_no']
    # Default ordering
    ordering = ['-prp_id']

class PR_Retrivee_APIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=PrProcessMaster.objects.all()
    serializer_class = PR_ProcessSerializer
    group_permissions = ['supply_chain']   
    ordering = ['-prp_id']

class ALLPR_APIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=PrProcessMaster.objects.filter(status="PENDING")
    serializer_class = PR_ProcessSerializer    
    group_permissions = ['supply_chain']   
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['created_date','status','prp_id']
    # Specify the fields by which the client can order the results
    ordering_fields = ['created_date','status','prp_id']
    # Default ordering
    ordering = ['-prp_id']
    
class user_lvl1_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]
    queryset=UserApproval.objects.filter(approver_level=1,approval=2)
    serializer_class = PR_UserApprovalSerializer

class user_lvl2_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=UserApproval.objects.filter(approver_level=2,approval=2)
    serializer_class = PR_UserApprovalSerializer
    
class PO_user_lvl1_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]
    queryset=UserApproval.objects.filter(approver_level=1,approval=1)
    serializer_class = PR_UserApprovalSerializer

class PO_user_lvl2_APIView(generics.ListAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=UserApproval.objects.filter(approver_level=2,approval=1)
    serializer_class = PR_UserApprovalSerializer



class PR_RetrieveAPIView(generics.RetrieveUpdateDestroyAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=PrProcessMaster.objects.all()
    serializer_class = PR_ProcessSerializer
    group_permissions = ['supply_chain']   
   

class PR_ApproverRetrieveAPIView(generics.RetrieveUpdateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=PurchRequistion.objects.all()
    serializer_class = PR_ApprovalSerializer  
    lookup_field='pr_id'
   
class RFQ_APIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=RfqMaster.objects.all()
    serializer_class = RFQ_Serializer
    group_permissions = ['supply_chain']   
    lookup_field='rfq_id'
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['created_date','vendor__vendor_name','vendor__vendor_email','vendor__vendor_city','vendor__vendor_mobile','rfq_no']
    # Specify the fields by which the client can order the results
    ordering_fields = ['created_date','vendor__vendor_name','vendor__vendor_email','vendor__vendor_city','vendor__vendor_mobile','rfq_no','type']
    # Default ordering
    ordering = ['-created_date']

    def get_queryset(self):
        type = self.request.query_params.get('type')
        queryset=self.queryset
        if type:
            return queryset.filter(type=type)
        return queryset
    def post(self, request, *args, **kwargs):
        serializer=RFQ_VendorSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():
            print("ok")
            serializer.save()
            return Response({"message":"sucessfully created"},status=status.HTTP_201_CREATED)
        else:
            # print(serializer.errors)    
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        # print(request.data)

class RFQ_RetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=RfqMaster.objects.all()
    serializer_class = RFQ_Serializer
    group_permissions = ['supply_chain']   
    lookup_field='rfq_id'

class PO_APIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=PoMaster.objects.all()
    serializer_class = PoSerializer
    group_permissions = ['supply_chain']   
    lookup_field='po_id'
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['created_date','po_no','status','prp__prp_no']
    # Specify the fields by which the client can order the results
    ordering_fields = ['created_date','po_no','status','prp__prp_no']
    # Default ordering
    ordering = ['-created_date']
class PO_RetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,YourPermission]
    queryset=PoMaster.objects.all()
    serializer_class = PoSerializer
    group_permissions = ['supply_chain']   
        
class PO_ApproverRetrieveAPIView(generics.RetrieveUpdateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=PoMaster.objects.all()
    serializer_class = PO_ApprovalSerializer  
    lookup_field='po_id'
class PO_ReturnRetrieveAPIView(generics.RetrieveUpdateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=PoMaster.objects.all()
    serializer_class = PO_ReturnSerializer  
    lookup_field='po_id'
      