from django.http import Http404
from django.shortcuts import render
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated , IsAdminUser

from vekaria_erp.settings import BASE_DIR
from .serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from authuser.permission import YourPermission 
from .models import *
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend
from .filters import *
from rest_framework import filters  
import json
# import pandas as pd
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    
class PartAPIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
  
    serializer_class = PartsSerializer
    group_permissions = ['inventory','quality']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PartsMasterFilter
    search_fields = ['product_part_name', 'product_part_no', 'category__c_name','source__s_name' ]
    # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','product_part_name','product_part_no','product_cost','category__c_name','product_source_type','is_active']
    # Default ordering
    ordering = ['product_part_no']
    lookup_field = 'part_id'  # Set the lookup field to 'part_id'

    def get_queryset(self):
        queryset = PartsMaster.objects.filter(product_type=1)
        # Get the filter parameters from the query parameters
        field = self.request.query_params.get('field')
        operator = self.request.query_params.get('operator')
        value = self.request.query_params.get('value')
        is_active = self.request.query_params.get('is_active')
        if is_active:
            queryset= PartsMaster.objects.filter(product_type=1,is_active=True)
        # Validate and apply filtering
        if field and operator and value:
            filter_param = f"{field}__{operator}"
            queryset = queryset.filter(**{filter_param: value})

        return queryset
class AllPartAPIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
  
    serializer_class = PartsSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PartsMasterFilter
    search_fields = ['product_part_name', 'product_part_no', 'category__c_name','product_descp' ]
    # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','product_part_name','product_part_no','product_cost','category__c_name','product_source_type','is_active']
    # Default ordering
    ordering = ['product_part_no']
    lookup_field = 'part_id'  # Set the lookup field to 'part_id'

    def get_queryset(self):
        queryset = PartsMaster.all_objects.filter(product_type=1)
        # Get the filter parameters from the query parameters
        field = self.request.query_params.get('field')
        operator = self.request.query_params.get('operator')
        value = self.request.query_params.get('value')
        is_active = self.request.query_params.get('is_active')
        if is_active:
            queryset= PartsMaster.objects.filter(product_type=1,is_active=True)
        # Validate and apply filtering
        if field and operator and value:
            filter_param = f"{field}__{operator}"
            queryset = queryset.filter(**{filter_param: value})

        return queryset

class PartRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsMaster.objects.filter(product_type=1)
    serializer_class = PartsSerializer
    group_permissions = ['inventory']
    lookup_field = 'part_id'  # Set the lookup field to 'part_id'
    def destroy(self, request, *args, **kwargs):
        part_id=kwargs.get('part_id')
        instance=super().get_object()
        if instance.product_pic_url is not None:
            
            cp=os.getcwd()
            del_path= str(cp + instance.product_pic_url)
            del_path= del_path.replace('\\','/')
            del_path= del_path.replace('%20',' ')
            del_path= del_path.replace('%40','@')
            print(instance.product_pic_url,del_path)
            try:
                os.remove(del_path)
            except Exception as e:
                print("delete product part pic error : ",e)
            
        return super().destroy(request, *args, **kwargs)
class AllPartRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsMaster.objects.filter(product_type=1)
    serializer_class = FullPartsSerializer
    group_permissions = ['inventory']
    lookup_field = 'part_id' 
    def destroy(self, request, *args, **kwargs):
        part_id=kwargs.get('part_id')
        instance=super().get_object()
        if instance.product_pic_url is not None:
            
            cp=os.getcwd()
            del_path= str(cp + instance.product_pic_url)
            del_path= del_path.replace('\\','/')
            del_path= del_path.replace('%20',' ')
            del_path= del_path.replace('%40','@')
            print(instance.product_pic_url,del_path)
            try:
                os.remove(del_path)
            except Exception as e:
                print("delete product part pic error : ",e)
            
        return super().destroy(request, *args, **kwargs)


class StoreLocationAPIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = StoreLocation.objects.all()
    serializer_class = StoreLocationSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
   
    search_fields = ['part__product_part_name', 'part__product_part_no', 'rack_no','row_no', 'shelf_no','tub_no']
    # Specify the fields by which the client can order the results
    ordering_fields = ['part__product_part_name', 'part__product_part_no', 'rack_no','row_no', 'shelf_no','tub_no']
    # Default ordering
    ordering = ['-store_location_id']
  
class StoreLocationRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = StoreLocation.objects.all()
    serializer_class = StoreLocationSerializer
    group_permissions = ['inventory']


class SubPartAPIView(generics.DestroyAPIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    group_permissions = ['inventory']
    serializer_class = SubPartSerializer
    queryset = SubpartMaster.objects.all()


class SubPartListAPIView(generics.ListAPIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    group_permissions = ['inventory']
    serializer_class = SubPartSerializer
    lookup_field = 'part_id' 
    def get_queryset(self):
        part_id = self.kwargs.get('part_id')
        queryset = SubpartMaster.objects.filter(part=part_id)
        return queryset



class MachineAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsMaster.objects.filter(product_type=3)
    serializer_class = MachineSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PartsMasterFilter
    search_fields = ['product_part_name', 'product_part_no', 'category__c_name', 'product_source_type']
    # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','product_part_name','product_part_no','product_cost','category__c_name','product_source_type']
    # Default ordering
    ordering = ['product_part_no']
    lookup_field = 'part_id'  # Set the lookup field to 'part_id'

    
class MachineRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsMaster.objects.filter(product_type=3)
    serializer_class = MachineSerializer
    lookup_field = 'part_id'  # Set the lookup field to 'part_id'
    group_permissions = ['inventory']

    def destroy(self, request, *args, **kwargs):
       
        instance=super().get_object()
        if instance.product_pic_url is not None:
            
            cp=os.getcwd()
            del_path= str(cp + instance.product_pic_url)
            del_path= del_path.replace('\\','/')
            del_path= del_path.replace('%20',' ')
            del_path= del_path.replace('%40','@')
            print(instance.product_pic_url,del_path)
            try:
                os.remove(del_path)
            except Exception as e:
                print("delete product_pic_url error : ",e)
            
        return super().destroy(request, *args, **kwargs)
    

class AssemblyAPIView(generics.ListCreateAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsMaster.objects.filter(product_type=2)
    serializer_class = AssemblySerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = PartsMasterFilter
    search_fields = ['product_part_name', 'product_part_no', 'category__c_name', 'product_source_type']
    # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','product_part_name','product_part_no','product_cost','category__c_name','product_source_type','product_pic_url','is_active']
    # Default ordering
    ordering = ['-part_id']

    lookup_field = 'part_id'  # Set the lookup field to 'part_id'

class AssemblyRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsMaster.objects.filter(product_type=2)
    serializer_class = AssemblySerializer
    lookup_field = 'part_id'  # Set the lookup field to 'part_id'

    group_permissions = ['inventory']

    def destroy(self, request, *args, **kwargs):
       
        instance=super().get_object()
        if instance.product_pic_url is not None:
            
            cp=os.getcwd()
            del_path= str(cp + instance.product_pic_url)
            del_path= del_path.replace('\\','/')
            del_path= del_path.replace('%20',' ')
            del_path= del_path.replace('%40','@')
            print(instance.product_pic_url,del_path)
            try:
                os.remove(del_path)
            except Exception as e:
                print("delete product_pic_url error : ",e)
            
        return super().destroy(request, *args, **kwargs)
    
class SourceAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = SourceMaster.objects.all()
    serializer_class = SourceSerializer
    group_permissions = ['inventory']
    
class SourceRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = SourceMaster.objects.all()
    serializer_class = SourceSerializer
    group_permissions = ['inventory']
class AllSourceAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = SourceMaster.all_objects.all()
    serializer_class = SourceSerializer
    group_permissions = ['inventory']
    
class AllSourceRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = SourceMaster.all_objects.all()
    serializer_class = SourceSerializer
    group_permissions = ['inventory']

class CategoryAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = CategoryMaster.objects.all()
    serializer_class = CategorySerializer
    group_permissions = ['inventory']
    # pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'c_name']
    # # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','is_active', 'c_name',]
    # # Default ordering
    ordering = ['-create_date']
class CategoryRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = CategoryMaster.objects.all()
    serializer_class = CategorySerializer
    group_permissions = ['inventory']
class AllCategoryAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = CategoryMaster.all_objects.all()
    serializer_class = CategorySerializer
    group_permissions = ['inventory']
    # pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'c_name']
    # # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','is_active', 'c_name',]
    # # Default ordering
    ordering = ['-create_date']
class AllCategoryRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = CategoryMaster.all_objects.all()
    serializer_class = CategorySerializer
    group_permissions = ['inventory']

class PartsVendorsAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsVendorsMaster.objects.all()
    serializer_class = PartsVendorsSerializer
    group_permissions = ['inventory']

class PartsVendorsAPIViewRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = PartsVendorsMaster.objects.all()
    serializer_class = PartsVendorsSerializer
    group_permissions = ['inventory']


class VendorsAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = VendorsMaster.objects.all()
    serializer_class = VendorSerializer
    group_permissions = ['inventory','quality']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'vendor_name', 'vendor_email', 'vendor_gst', 'vendor_mobile']
    # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','vendor_name', 'vendor_email', 'vendor_gst', 'vendor_mobile']
    # Default ordering
    ordering = ['-create_date']

class VendorsRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = VendorsMaster.objects.all()
    serializer_class = VendorSerializer
    group_permissions = ['inventory','quality']
class AllVendorsAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = VendorsMaster.all_objects.all()
    serializer_class = VendorSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'vendor_name', 'vendor_email', 'vendor_gst', 'vendor_mobile']
    # Specify the fields by which the client can order the results
    ordering_fields = ['create_date','vendor_name', 'vendor_email', 'vendor_gst', 'vendor_mobile']
    # Default ordering
    ordering = ['-create_date']

class AllVendorsRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = VendorsMaster.all_objects.all()
    serializer_class = VendorSerializer
    group_permissions = ['inventory']

class GetPartsVendorAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    serializer_class = PartsVendorsSerializer
    group_permissions = ['inventory','quality']
   
    def get_queryset(self):
        part_id = self.kwargs.get('pk')
        print('partid==>',part_id)
        queryset= PartsVendorsMaster.objects.filter(part=part_id)
        print("partvendor=>",PartsVendorsMaster.objects.filter(part=part_id))
        return queryset   



class Purch_InwardAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = PurchMaster.objects.all()
    serializer_class = PurchInwardSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'mrr_no','vendor_inv_no','invoice_dt','vendor__vendor_name','vendor_po']
    # Specify the fields by which the client can order the results
    ordering_fields = ['mrr_no','vendor_inv_no','invoice_dt','vendor__vendor_name']
    # Default ordering
    ordering = ['-created_date']
    
class Purch_InwardRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = PurchMaster.objects.all()
    serializer_class = PurchInwardSerializer
    group_permissions = ['inventory']
  


class ShopfloorAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = ShopFloorMaster.objects.all()
    serializer_class = ShopfloorSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'min_no','from_department','prepared_by','auth_by']
    # Specify the fields by which the client can order the results
    ordering_fields = ['min_no','from_department','prepared_by','auth_by']
    # Default ordering
    ordering = ['-created_date']
    
class ShopfloorRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = ShopFloorMaster.objects.all()
    serializer_class = ShopfloorSerializer
    group_permissions = ['inventory']
  

class Shpofloor_ApproverRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=ShopFloorMaster.objects.all()
    serializer_class = ShopfloorApprovalSerializer  
    lookup_field='mat_sf_id'
class ShpofloorReturnRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset=ShopFloorMaster.objects.all()
    serializer_class = ShopfloorReturnSerializer  
    lookup_field='mat_sf_id'


class ShopfloorAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = ShopFloorMaster.objects.all()
    serializer_class = ShopfloorSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'min_no','from_department','prepared_by','auth_by','created_date']
    # Specify the fields by which the client can order the results
    ordering_fields = ['min_no','from_department','prepared_by','auth_by','created_date']
    
    ordering = ['-created_date']
    def get_queryset(self):
        filter= self.request.query_params.get("status")
        queryset = ShopFloorMaster.objects.all()
        if filter:
            queryset=ShopFloorMaster.objects.filter(status=filter)
        return queryset
    
class MrLastAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
      
        
        try:
            l_mrs_id = MrsMaster.objects.latest('mrs_no')
        except MrsMaster.DoesNotExist:
            l_mrs_id=None
     
        new_mrs_id =  1

        latest_mrs_no = l_mrs_id.mrs_no if l_mrs_id else None     
        if latest_mrs_no:  
            # Increment the latest mrs_id by 1
            current_mrs_id = int(latest_mrs_no[3:])
            new_mrs_id = current_mrs_id + 1
            print(new_mrs_id)
        formatted_mrs_id = 'MRS{:04d}'.format(new_mrs_id)
        return Response({"mrs_no":formatted_mrs_id})
class MinLastAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        
        try:
            l_min_id = MrsMaster.objects.latest('min_no')
        except MrsMaster.DoesNotExist:
            l_min_id=None
       
        new_min_id =  1

        latest_min_no = l_min_id.min_no if l_min_id else None     
        if latest_min_no:  
            # Increment the latest mrs_id by 1
            current_min_id = int(latest_min_no[3:])
            new_min_id = current_min_id + 1
            print(new_min_id)
        formatted_mrs_id = 'MIN{:04d}'.format(new_min_id)
        return Response({"min_no":formatted_mrs_id})
    
class CisLastAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            l_min_id = MrsMaster.objects.latest('min_no')
        except MrsMaster.DoesNotExist:
            l_min_id=None
       
        new_min_id =  1

        latest_min_no = l_min_id.min_no if l_min_id else None     
        if latest_min_no:  
            # Increment the latest mrs_id by 1
            current_min_id = int(latest_min_no[3:])
            new_min_id = current_min_id + 1
            print(new_min_id)
       
        formatted_mrs_id = 'CIS{:04d}'.format(new_min_id)
        return Response({"cis_no":formatted_mrs_id})
    
  
class MrsAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = MrsMaster.objects.filter(type=0)
    serializer_class = Mrs_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['mrs_no', 'from_dept__dept_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'mrs_no','mrs_date','from_dept__dept_name']
    # Default ordering
    ordering = ['-created_date']    
    lookup_field = 'mrs_no'  # Set the lookup field to 'mrs_id'

class MrsPendingAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = MrsMaster.objects.filter(status=False,type=0)
    serializer_class = Mrs_Serializers   
    group_permissions = ['inventory']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['mrs_no', 'from_dept__dept_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'mrs_no','mrs_date','from_dept__dept_name']
    # Default ordering
    ordering = ['-created_date']    
    lookup_field = 'mrs_no'  # Set the lookup field to 'mrs_id'
    
class MrsRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = MrsMaster.objects.filter(type=0)
    serializer_class = Mrs_Serializers
    group_permissions = ['inventory']
    lookup_field = 'mrs_no'  # Set the lookup field to 'mrs_id'
    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     lookup_value = self.kwargs[self.lookup_field]

    #     try:
    #         obj = queryset.get(**{self.lookup_field: lookup_value})
    #     except queryset.model.DoesNotExist:
    #         raise Http404("No {} matches the given query.".format(queryset.model._meta.object_name))
    #     except queryset.model.MultipleObjectsReturned:
    #         obj = queryset.filter(**{self.lookup_field: lookup_value}).first()

    #     # self.check_object_permissions(self.request, obj)
    #     return obj
class MinAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = MrsMaster.objects.filter(type=0)
    serializer_class = Min_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'mrs_no','mrs_date','from_dept__dept_name',]
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'mrs_no','mrs_date','from_dept__dept_name']
    # Default ordering
    ordering = ['-created_date']   
    lookup_field = 'mrs_no'  # Set the lookup field to 'mrs_id'
class MinIssuedAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = MrsMaster.objects.filter(status=True,type=0)
    serializer_class = Min_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'mrs_no','mrs_date','from_dept__dept_name',]
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'mrs_no','mrs_date','from_dept__dept_name']
    # Default ordering
    ordering = ['-created_date']   
    lookup_field = 'mrs_no'  # Set the lookup field to 'mrs_id'

class MinRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset =  MrsMaster.objects.filter(type=0)
    serializer_class = Min_Serializers
    group_permissions = ['inventory']
    lookup_field = 'mrs_no'  # Set the lookup field to 'mrs_id'

class CISAPIView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = MrsMaster.objects.all()
    serializer_class = CIS_Serializers
    group_permissions = ['inventory']

class StockAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    # queryset = StockMaster.objects.all()
    serializer_class = Stock_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    ordering_fields = [ 'stock_id',]
    ordering = ['-stock_id']   
    def get_queryset(self):
        request=self.request
        category = request.query_params.get('category') 
        print(category) # Get the 'category' parameter from the URL
        if category:
            return StockMaster.objects.filter( part__is_active=True, part__category__c_name=category)
        
        return StockMaster.objects.filter( part__is_active=True)
    

class PartStockAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    
    serializer_class = Stock_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_id',]
    # Default ordering
    ordering = ['-stock_id']  
    def get_queryset(self):
        request=self.request
        category = str(request.query_params.get('category')).lower() if request.query_params.get('category') else None # Get the 'category' parameter from the URL
        
        if category=='raw material':
            return StockMaster.objects.filter(type=2)
        elif category:
            return StockMaster.objects.filter( part__is_active=True, part__category__c_name=category)
 
        # Return the default queryset if 'category' is not present in the URL
        return StockMaster.objects.filter(part__product_type=1, part__is_active=True)  
class AssemblyStockAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]

    serializer_class = Stock_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_id',]
    # Default ordering
    ordering = ['-stock_id']    
    def get_queryset(self):
        request=self.request
        category = request.query_params.get('category')  # Get the 'category' parameter from the URL
        if category:
            # Filter the queryset by category if it is present in the URL
            return StockMaster.objects.filter(part__product_type=2, part__is_active=True, part__category__c_name=category)
        # Return the default queryset if 'category' is not present in the URL
        return StockMaster.objects.filter(part__product_type=2, part__is_active=True)


class Raw_MatStockAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]

    serializer_class = Stock_Serializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'rm__rm_mat_name','rm__rm_mat_code','rm__rm_mat_desc','rm__rm_sec_type','stock_avail','stock_ui']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_id','rm__rm_mat_name','rm__rm_mat_code','rm__rm_mat_desc','rm__rm_sec_type','stock_avail','stock_ui']
    # Default ordering
    ordering = ['-stock_id']    
    def get_queryset(self):
        return StockMaster.objects.filter(type=2)
class StockRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = StockMaster.objects.all()
    serializer_class = Stock_Serializers
    group_permissions = ['inventory']


class ReserveStockAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    # queryset = StockMaster.objects.all()
    serializer_class = Stock_ReservSerialiser
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_reserv_id',]
    # Default ordering
    ordering = ['-stock_reserv_id']   
    def get_queryset(self):
        request=self.request
        category = request.query_params.get('category')  # Get the 'category' parameter from the URL
        if category:
            return StockReserv.objects.filter( part__is_active=True, part__category__c_name=category)

        return StockReserv.objects.filter( part__is_active=True)
class PartReserveStockAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    
    serializer_class = Stock_ReservSerialiser
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_reserv_id',]
    # Default ordering
    ordering = ['-stock_reserv_id']  
    def get_queryset(self):
        request=self.request
        category = request.query_params.get('category')  # Get the 'category' parameter from the URL
        if category:
            # Filter the queryset by category if it is present in the URL
            return StockReserv.objects.filter(part__product_type=1, part__is_active=True, part__category__c_name=category)
        # Return the default queryset if 'category' is not present in the URL
        return StockReserv.objects.filter(part__product_type=1, part__is_active=True)  
class AssemblyReserveStockAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]

    serializer_class = Stock_ReservSerialiser
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_reserv_id',]
    # Default ordering
    ordering = ['-stock_reserv_id']    
    def get_queryset(self):
        request=self.request
        category = request.query_params.get('category')  # Get the 'category' parameter from the URL
        if category:
            # Filter the queryset by category if it is present in the URL
            return StockReserv.objects.filter(part__product_type=2, part__is_active=True, part__category__c_name=category)
        # Return the default queryset if 'category' is not present in the URL
        return StockReserv.objects.filter(part__product_type=2, part__is_active=True)
class MaterialReserveStockAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]

    serializer_class = Stock_ReservSerialiser
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'part__product_part_no','part__product_part_name']
    # Specify the fields by which the client can order the results
    ordering_fields = [ 'stock_reserv_id',]
    # Default ordering
    ordering = ['-stock_reserv_id']    
    def get_queryset(self):
        request=self.request
       
        return StockReserv.objects.filter(type=2)



class ReserveStockRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes =  [IsAuthenticated,YourPermission]
    queryset = StockReserv.objects.all()
    serializer_class = Stock_ReservSerialiser
    group_permissions = ['inventory']


class RawMaterialAPIView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=RawMaterialMaster.objects.all()
    serializer_class=Raw_MaterialSerializers
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['rm_mat_code','rm_sec_type','rm_mat_name','rm_size','rm_stock_free','rm_stock_res']
    # Specify the fields by which the client can order the results
    ordering_fields = ['rm_id', 'rm_mat_name','rm_sec_type','rm_size','rm_stock_free','rm_stock_res']
    # Default ordering
    ordering = ['-rm_id']    
    
class RawMaterialRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=RawMaterialMaster.objects.all()
    serializer_class=Raw_MaterialSerializers
    group_permissions = ['inventory']

class DepartmentAPIView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=DepartmentMaster.objects.all()
    serializer_class=DepartmentSerializer
    group_permissions = ['inventory']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'dept_name']
    # Specify the fields by which the client can order the results
    ordering_fields = ['dept_name']
    # Default ordering
    ordering = ['-dept_id']    
    
class DepartmentRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=DepartmentMaster.objects.all()
    serializer_class=DepartmentSerializer
    group_permissions = ['inventory']

class PurchRequistAPIView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,YourPermission]
    queryset=PurchRequistion.objects.all()
    serializer_class=PurchRequistSerializer
    group_permissions = ['inventory','production','production_planning']
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = [ 'pr_no','pr_date','dept__dept_name','req_by_date']
    ordering_fields = ['pr_no','pr_date','dept__dept_name','req_by_date']
    ordering = ['-pr_id']    
    
    def get_queryset(self):
        queryset=PurchRequistion.objects.all()
        stat = self.request.query_params.get('pr_status')
        if stat:
            queryset=PurchRequistion.objects.filter(pr_status=stat)
        return queryset
    
class PurchrequistLastAPIView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        try:
            pr_id = PurchRequistion.objects.latest('pr_no')
        except PurchRequistion.DoesNotExist:
            pr_id=None
       
        new_pr_id =  1

        latest_pr_no = pr_id.pr_no if pr_id else None     
        if latest_pr_no:  
            # Increment the latest pr by 1
            current_pr_id = int(latest_pr_no[2:])
            new_pr_id = current_pr_id + 1
            print(new_pr_id)
        formatted_pr_id = 'PR{:04d}'.format(new_pr_id)
        return Response({"pr_no":formatted_pr_id})
class PurchRequistRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated,YourPermission]
    queryset=PurchRequistion.objects.all()
    serializer_class=PurchRequistSerializer
    group_permissions = ['production','production','production_planning']


class PurchRequistReturnRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=PurchRequistion.objects.all()
    serializer_class=PurchRequistReturnSerializer
    group_permissions = ['production','production','production_planning'
                         ]


class Raw_VendorAPIView(generics.ListCreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    queryset=RmVendorMaster.objects.all()
    serializer_class=Raw_VendorSerializers
     
class Raw_UpdateVendorAPIView(generics.RetrieveUpdateDestroyAPIView):
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated,YourPermission]
    queryset=RmVendorMaster.objects.all()
    serializer_class=Raw_VendorSerializers
   
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance,instance.rm_vendor_datasheet_url)
        if instance.rm_vendor_datasheet_url:
            try:
                cp=os.getcwd()
                print("cp",cp)
                file_path =cp+ instance.rm_vendor_datasheet_url
                print("path",file_path)
                os.remove(file_path)
            except Exception as e:
                pass
        if instance.catalog_url:
            try:
                cp=os.getcwd()
                print("cp",cp)
                file_path =cp+ instance.catalog_url
                print("path",file_path)
                os.remove(file_path)
            except Exception as e:
                pass
        if instance.quotation_url:
            try:
                cp=os.getcwd()
                print("cp",cp)
                file_path =cp+ instance.quotation_url
                print("path",file_path)
                os.remove(file_path)
            except Exception as e:
                pass
        return super().destroy(request, *args, **kwargs)


class GetRMVendorAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    serializer_class = Raw_VendorSerializers
    group_permissions = ['inventory']
   
    def get_queryset(self):
        rm_id = self.kwargs.get('pk')
        queryset= RmVendorMaster.objects.filter(rm__rm_id=rm_id)
        return queryset    

# class raw_mat_data(APIView):
#     def get(self,request):
#         print(BASE_DIR)
#         excel_file_path = os.path.join(BASE_DIR, 'RawMaterial.xlsx')
#         if os.path.exists(excel_file_path):
#             df = pd.read_excel(excel_file_path,sheet_name='Sheet2')
#             print(df)
           
#             for index, row in df.iterrows():
#                 Size=None
#                 if row['Size'] is not 'nan' or row['Size'] is not None:
#                     Size=row['Size']
#                 RawMaterialMaster.objects.create(rm_mat_name=row['Type'],rm_mat_code=index+1,rm_mat_desc=row['Unnamed: 0'],rm_sec_type=row['Section'],rm_size=Size,created_date=timezone.now(),modify_date=timezone.now())
               
#             return Response({'message':f"ok"})

#     # Your further processing with the DataFrame
#         else:
#             print(f"The file {excel_file_path} does not exist.")
#             return Response({'message':f"The file {excel_file_path} does not exist."})
# class vendorentry(APIView):
#     def get(self,request):
#         vendor= ErpCustomermaster.objects.filter(cc_categoryid='1011')
#         for vendordata in vendor:
#             print(vendordata)
#             city_name= ErpCitymaster.objects.get(cm_cityid=vendordata.cm_cityid)
#             VendorsMaster.objects.create(vendor_name=vendordata.cm_customername,vendor_city=city_name.cm_cityname
#                                          ,vendor_gst=vendordata.cm_gstno,
#                                          vendor_email=vendordata.cm_email
#                                          ,vendor_address=vendordata.cm_addressline1
#                                          ,vendor_address_2=vendordata.cm_addressline2
#                                          ,vendor_address_3=vendordata.cm_addressline3
#                                          ,vendor_address_4=vendordata.cm_addressline4
#                                         ,vendor_mobile=vendordata.cm_mobile
#                                         ,create_date=timezone.now(),
#                                         modify_date=timezone.now(),
#                                          is_active=True)
            
#         return Response({"message":"OK"})
# class stockrmcreate(APIView):
#     def get(self,request):
#         rm=RawMaterialMaster.objects.all()
#         for rms in rm:
#             if not StockMaster.objects.filter(rm=rms.rm_id).exists() :
#                 print("pms.pm_productcode : ")
#                 StockMaster.objects.create(rm=rms,type=2,stock_avail=0,stock_ui=0,stock_reserv=0,stock_rej=0,last_update=timezone.now())

#         return Response({"message":"OK"})

# class stockcreate(APIView):
#     def get(self,request):
#         pm= PartsMaster.objects.filter(product_type__in=[1,2])
#         for pms in pm:
#             if not StockMaster.objects.filter(part=pms.part_id).exists() :
#                 print("pms.pm_productcode : ",pms.product_part_name)
#                 StockMaster.objects.create(part=pms,stock_avail=0,stock_ui=0,stock_reserv=0,stock_rej=0,last_update=timezone.now(),type=1)

#         return Response({"message":"OK"})
# class Reservstockcreate(APIView):
#     def get(self,request):
#         pm= StockMaster.objects.all()
#         for pms in pm:
#             if not StockReserv.objects.filter(part=pms.part).exists() :
#                 print("pms.pm_productcode : ",pms.part)
#                 StockReserv.objects.create(part=pms.part,reserve_qty=0,issue_qty=0)

#         return Response({"message":"OK"})
# class ReservRmstockcreate(APIView):
#     def get(self,request):
#         rm=RawMaterialMaster.objects.all()
#         for rms in rm:
#             if not StockReserv.objects.filter(rm=rms.rm_id).exists() :
              
#                 StockReserv.objects.create(rm=rms,type=2,reserve_qty=0,issue_qty=0)

#         return Response({"message":"OK"})
# import data ErpProductmaster to PartsMaster 
# class partlist(APIView):
#     def get(self,request):
#         pm= PartsMaster.objects.all()
#         for pms in pm:
#             if  PartsMaster.objects.filter(part_id=pms.part_id).exists() :
#                 if pms.product_pic_url:
#                     PartsMaster.objects.filter(part_id=pms.part_id).update(product_pic_url=f"/media/{pms.product_pic_url}")
#                 print("pms. url : ",pms.product_pic_url)
                                                    
#         return Response({"message":"OK"})
# class partlist(APIView):
#     def get(self,request):
#         pm= ErpProductmaster.objects.filter(pm_producttype=1)
#         for pms in pm:
#             if not PartsMaster.objects.filter(product_part_no=pms.pm_productcode).exists() :
#                 print("pms.pm_productcode : ",pms.pm_productname)
#                 PartsMaster.objects.create(product_part_no=pms.pm_productcode,product_part_name=str(pms.pm_productname),product_descp=pms.pm_productdesc,
#                 product_category=None,product_cost=pms.pm_rate,hsn_code=pms.pm_hsmnumber,product_drawing_no=pms.pm_drawbackno,
#                                           create_date=datetime.now(),create_by=1       ,                       is_active=True                                                                )

#         return Response({"message":"OK"})
