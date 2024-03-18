import json
from django.http import HttpRequest
from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date
from django.utils import timezone
from .models import *
import os
from authuser.models import AuthUser, UserApproval
from django.db.models import Q, F
from django.db.models import Max
import re
from .model_manager import *
from rest_framework.exceptions import ValidationError
from django.db import transaction
  

class StockUpdate_Serializers(serializers.ModelSerializer):
    class Meta:
        model = StockUpdate
        exclude = []

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class Stock_Serializers(serializers.ModelSerializer):
    class Meta:
        model = StockMaster
        exclude = []
        extra_kwargs = {
            "stock_rej": {
                "default": 0
            },
            "stock_avail": {
                "default": 0
            },
            "stock_ui": {
                "default": 0
            },
            "stock_reserv": {
                "default": 0
            },
        }

    def to_representation(self, instance: StockMaster):

        data = super().to_representation(instance)
        # request: HttpRequest = self.context.get('request')

        # # Check if the filter parameter 'kwargs_filter' is present in the URL
        # category = request.query_params.get('category')
        # print(request)
        # path_parts = request.path.split('/')
        # if 'assembly' in path_parts:
        #      pass
        if instance.part:
            part = PartsMaster.objects.filter(part_id=instance.part.part_id, is_active=True).values('part_id', 'product_part_no', 'product_part_name', 'product_descp', 'product_pic_url', 'product_type', 'uom',
                                                                                                    'product_cost', 'category_id', 'minimum_stock_qty')
            # print(part)
            if part.exists():
                part_data = part[0]
                data.update(part_data)
        else:
            data['rm_mat_code']=instance.rm.rm_mat_code
            data['rm_mat_name']=instance.rm.rm_mat_name
            data['rm_mat_desc']=instance.rm.rm_mat_desc
            data['rm_size']=instance.rm.rm_size
            data['rm_sec_type']=instance.rm.rm_sec_type
            data['rm_stock_free']=instance.rm.rm_stock_free
            data['rm_stock_res']=instance.rm.rm_stock_res
            data['part_id']=instance.part
               
            
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance:StockMaster, validated_data):
        validated_data['last_update']=timezone.now()
        requestuser = self.context['request'].user
        validated_data['updt_by']=requestuser.id
        stock = super().update(instance, validated_data)
        if validated_data.get('part'):
            serializer = StockUpdate_Serializers(data={

                "part": instance.part.part_id,
                "stock_avail": stock.stock_avail,
                "stock_ui": stock.stock_ui,
                "stock_reserv": stock.stock_reserv,
                "stock_rej": stock.stock_rej,
                "updt_date": timezone.now(),
                "updt_by": requestuser.id,
                "tran_type": "Update",
                "type": 1,

                "remarks": stock.remarks
            })
            if serializer.is_valid():
                serializer.save()
            else:
                print("stock Update add error => ", serializer.errors)
        if validated_data.get('rm'):
            serializer = StockUpdate_Serializers(data={

                "rm": instance.rm.rm_id,
                "stock_avail": stock.stock_avail,
                "stock_ui": stock.stock_ui,
                "stock_reserv": stock.stock_reserv,
                "stock_rej": stock.stock_rej,
                "updt_date": timezone.now(),
                "updt_by": requestuser.id,
                "tran_type": "Update",
                "type": 2,
                "remarks": stock.remarks
            })
            if serializer.is_valid():
                serializer.save()
            else:
                print("stock Update add error => ", serializer.errors)
        return stock


class Stock_ReservSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StockReserv
        exclude = []

    def to_representation(self, instance: StockReserv):

        data = super().to_representation(instance)
        # request: HttpRequest = self.context.get('request')

        # # Check if the filter parameter 'kwargs_filter' is present in the URL
        # category = request.query_params.get('category')
        # print(request)
        # path_parts = request.path.split('/')
        stock = StockMaster.objects.filter(part=instance.part.part_id)
        if stock.exists():
            stock_avail = stock[0].stock_avail
            data.update({"stock_avail": stock_avail})
        else:
            data.update({"stock_avail": 0})

        part = PartsMaster.objects.filter(part_id=instance.part.part_id, is_active=True).values('part_id', 'product_part_no', 'product_part_name', 'product_descp', 'product_pic_url', 'product_type', 'uom',
                                                                                                'product_cost', 'product_type')
        # print(part)
        if part.exists():
            part_data = part[0]
            data.update(part_data)
        return data

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):

        validated_data.pop('trans_type', None)
        Resvstock = super().update(instance, validated_data)
        requestuser = self.context['request'].user

        if StockMaster.objects.filter(part=validated_data.get('part')).exists():
            stock = StockMaster.objects.get(part=validated_data.get('part'))
            stock.stock_reserv = validated_data.get('reserve_qty')
            if stock.stock_avail > validated_data.get('reserve_qty'):
                serializers.ValidationError(
                    {"reserve_qty": "Higher reserve quantity than free quantity"})
            if stock.stock_avail or stock.stock_avail < 0:
                stock.stock_avail = int(
                    stock.stock_avail)-int(validated_data.get('reserve_qty'))
            stock.save()
            serializer = StockUpdate_Serializers(data={
                "part": instance.part.part_id,
                "stock_avail": stock.stock_avail,
                "stock_ui": stock.stock_ui,
                "stock_reserv": stock.stock_reserv,
                "stock_rej": stock.stock_rej,
                "updt_date": timezone.now(),
                "updt_by": requestuser.id,
                "tran_type": "Reservation",

                "remarks": stock.remarks
            })
            if serializer.is_valid():
                serializer.save()
            else:
                print("stock Update add error => ", serializer.errors)

        return Resvstock


class StoreLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StoreLocation
        exclude = []

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class FullPartsSerializer(serializers.ModelSerializer):
    product_pic_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    specification_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_product_pic = serializers.BooleanField(
        default=False, required=False, write_only=True)
    del_specification = serializers.BooleanField(
        default=False, required=False, write_only=True)
    drawing_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_drawing_pic = serializers.BooleanField(
        default=False, required=False, write_only=True)
    row_no = serializers.CharField(required=False, write_only=True)
    rack_no = serializers.CharField(required=True, write_only=True)
    shelf_no = serializers.CharField(required=False, write_only=True)
    tub_no = serializers.CharField(required=True, write_only=True)
    remark = serializers.CharField(required=False, write_only=True)
    class Meta:
        model = PartsMaster
        field = ['__all__', 'product_pic_upload', 'drawing_upload','del_specification',
                 'del_drawing_pic', 'row_no', 'rack_no', 'shelf_no', 'remark']
        extra_kwargs = {
            "product_pic_url": {
                "required": False
            },
            "product_drawing_no": {
                "required": False

            },
            "modify_date": {
                "required": False

            },
            "modify_by": {
                "required": False

            },
            "aproved_by": {
                "required": False

            },
            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },
            "is_active": {
                "required": False,
                "default": True
            }
        }
        exclude = []

    def validate_product_part_no(self, value):
        part = self.instance  # Get the current assemblies instance being updated
        if part is not None and str(part.product_part_no).strip() == str(value).strip():
            return value  # a_no not changed, no need to perform validation

        if PartsMaster.objects.filter(product_part_no=value).exists():
            raise serializers.ValidationError(
                "This Part no is already in use.")
        return value

    def to_representation(self, instance: PartsMaster):
        representation = super().to_representation(instance)
        product_category = instance.category
        category_name = getattr(product_category, 'c_name', None)
        store_values = StoreLocation.objects.filter(
            part=instance.part_id).values()

        store_data = list(store_values)
        for store_item in store_data:
            representation.update(store_item)
        if StockMaster.objects.filter(part=instance.part_id).exists():
            stock_avail=StockMaster.objects.get(part=instance.part_id)
            
            representation['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
        else:
                            representation['stock_avail'] = 0
        representation['product_category_name'] = category_name

        return representation

    def create(self, validated_data):
        # Retrieve necessary data from validated_data
        request = {"request": self.context['request']}

        product_pic_upload = validated_data.get('product_pic_upload', None)
        drawing_upload = validated_data.get('drawing_upload', None)
        row_no = validated_data.get('row_no', None)
        rack_no = validated_data.get('rack_no', None)
        shelf_no = validated_data.get('shelf_no', None)
        tub_no = validated_data.get('tub_no', None)
        remark = validated_data.get('remark', None)
        product_pic_url = None
        draw_pic_url = None
        print(validated_data)
        # Get the user making the request
        requestuser = self.context['request'].user
        # STORE LOCATION
        validated_data.pop('del_specification',None)
        validated_data.pop('row_no', None)
        validated_data.pop('rack_no', None)
        validated_data.pop('shelf_no', None)
        validated_data.pop('tub_no', None)
        validated_data.pop('remark', None)
        # Set initial values
        validated_data['product_type'] = 1
        validated_data.pop('drawing_upload', None)
        specification_upload=validated_data.pop('specification_upload', None)
        validated_data.pop('del_product_pic', False)
        validated_data.pop('del_drawing_pic', False)
        validated_data.pop('product_pic_upload', None)
        validated_data['create_date'] = timezone.now()
        validated_data['create_by'] = requestuser.id

        # Call the superclass's create method to create a new product instance
        part = super().create(validated_data)
        # part add in  stock

        serializer = Stock_Serializers(data={"part": part.part_id,"type":1})
        if serializer.is_valid():
            serializer.save()
        else:
            print("stock add error => ", serializer.errors)
        print("part_no ", part.part_id)

        # Handle product picture upload
        if product_pic_upload is not None and len(product_pic_upload) != 0:
            fs = FileSystemStorage()
            product_pic_upload_name = product_pic_upload.name.replace(' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_' +validated_data.get('product_part_no')+product_pic_upload_name}", product_pic_upload)
            else:
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_'+product_pic_upload_name}", product_pic_upload)
            product_pic_url = fs.url(filename)

        # Handle drawing upload
        if drawing_upload is not None and len(drawing_upload) != 0:
            fs = FileSystemStorage()
            drawing_upload_name = drawing_upload.name.replace(' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_'+validated_data.get('product_part_no')+drawing_upload_name}", drawing_upload)
            else:
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_' +drawing_upload_name}")
            draw_pic_url = fs.url(filename)
        if specification_upload is not None and len(specification_upload) != 0:
            fs = FileSystemStorage()
            try:
                specification_upload_name = specification_upload.name.replace(' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(
                        f"Uploads/Parts/{str(part.part_id)+'_'+validated_data.get('product_part_no')+specification_upload_name}", specification_upload)
                else:
                    filename = fs.save(
                        f"Uploads/Parts/{str(part.part_id)+'_' +specification_upload_name}")
                specification_upload_url = fs.url(filename)
                validated_data['specification_upload'] = specification_upload_url
            except Exception as e:
                print("Exception raise=>",e)
        # Update the validated_data dictionary with image URLs
        validated_data['product_pic_url'] = product_pic_url
        validated_data['drawing_img'] = draw_pic_url
        partobj = PartsMaster.all_objects.get(part_id=part.part_id)
        storeloc = {
            "part": partobj.part_id,
            "row_no": row_no,
            "rack_no": rack_no,
            "shelf_no": shelf_no,
            "tub_no": tub_no,
            "remark": remark
        }
        serializer = StoreLocationSerializer(data=storeloc, context=request)
        if serializer.is_valid():
            print("store loc =>", storeloc)
            serializer.save()
        else:
            print("store loc error =>", serializer.errors)

        partupdate = super().update(partobj, validated_data)
        return partupdate

    def update(self, instance, validated_data):
        product_pic_upload = validated_data.get('product_pic_upload', None)
        del_pic = validated_data.get('del_product_pic', False)
        drawing_upload = validated_data.get('drawing_upload', None)
        del_drawing_pic = validated_data.get('del_drawing_pic', False)
        del_specification = validated_data.get('del_specification', False)
        request = {"request": self.context['request']}
        specification_upload=validated_data.pop('specification_upload', None)
        specification_upload=validated_data.pop('specification_upload', None)

        product_part_no = validated_data.get(
            'product_part_no', instance.product_part_no)
        print(validated_data)
        if del_pic:
            if instance.product_pic_url != None:
                cp = os.getcwd()
                p = str(cp + instance.product_pic_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete product_pic_url img error :", e)
                instance.product_pic_url = None
                instance.save()
        if del_drawing_pic:
            if instance.drawing_img != None:
                cp = os.getcwd()
                p = str(cp + instance.drawing_img)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete drawing_img  error :", e)
                instance.drawing_img = None
                instance.save()
        if del_specification:
            if instance.specification_upload != None:
                cp = os.getcwd()
                p = str(cp + instance.specification_upload)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete drawing_img  error :", e)
                instance.specification_upload = None
                instance.save()
        requestuser = self.context['request'].user

        if product_pic_upload != None:
            if len(product_pic_upload) != 0:
                # delete old product pic url
                if instance.product_pic_url != None:
                    cp = os.getcwd()
                    p = str(cp + instance.product_pic_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete product part img error :", e)

                fs = FileSystemStorage()
                product_pic_upload_name = product_pic_upload.name.replace(
                    ' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id)+'_'+validated_data.get('product_part_no')+product_pic_upload_name}",
                                       product_pic_upload)
                else:

                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id) +'_'+ instance.product_part_no}",
                                       product_pic_upload)

                product_pic_url = fs.url(filename)
                validated_data['product_pic_url'] = product_pic_url
        
        if drawing_upload != None:
            if len(drawing_upload) != 0:
                if instance.drawing_img != None:
                    cp = os.getcwd()
                    p = str(cp + instance.drawing_img)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete drawing_img img error :", e)

                fs = FileSystemStorage()
                drawing_img_name = drawing_upload.name
                drawing_img_name = drawing_img_name.replace(' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id)+'_' +validated_data.get('product_part_no')+drawing_img_name}",
                                       drawing_upload)
                else:
                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id)+'_' +instance.product_part_no+drawing_img_name}",
                                       drawing_upload)

                draw_img_url = fs.url(filename)
                validated_data['drawing_img'] = draw_img_url

        if specification_upload is not None and len(specification_upload) != 0:
            fs = FileSystemStorage()
            if instance.specification_upload != None:
                    cp = os.getcwd()
                    p = str(cp + instance.specification_upload)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete drawing_img img error :", e)

            try:
                specification_upload_name = specification_upload.name.replace(' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(
                        f"Uploads/Parts/{str(instance.part_id)+'_'+validated_data.get('product_part_no')+specification_upload_name}", specification_upload)
                else:
                    filename = fs.save(
                        f"Uploads/Parts/{str(instance.part_id)+'_' +specification_upload_name}")
                specification_upload_url = fs.url(filename)
                validated_data['specification_upload'] = specification_upload_url
                
            except Exception as e:
                print("Exception raise=>",e)
        
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        if validated_data.get('is_active') == False:
            validated_data['closed_by'] = requestuser.id

        del_drawing_pic = validated_data.pop('del_drawing_pic', False)
        drawing_upload = validated_data.pop('drawing_upload', None)
        if StoreLocation.objects.filter(part=instance).exists():
            row_no = validated_data.get('row_no', None)
            rack_no = validated_data.get('rack_no', None)
            shelf_no = validated_data.get('shelf_no', None)
            tub_no = validated_data.get('tub_no', None)
            remark = validated_data.get('remark', None)
            storeinstance = StoreLocation.objects.get(part=instance)
            storeloc = {
                "part": instance.part_id,
                "row_no": row_no,
                "rack_no": rack_no,
                "shelf_no": shelf_no,
                "tub_no": tub_no,
                "remark": remark
            }
            serializer = StoreLocationSerializer(
                instance=storeinstance, data=storeloc, context=request)
            if serializer.is_valid():
                print("store loc =>", storeloc)
                serializer.save()
            else:
                print("store loc error => ", serializer.errors)
        else:
            row_no = validated_data.get('row_no', None)
            rack_no = validated_data.get('rack_no', None)
            shelf_no = validated_data.get('shelf_no', None)
            tub_no = validated_data.get('tub_no', None)
            remark = validated_data.get('remark', None)

            storeloc = {
                "part": instance.part_id,
                "row_no": row_no,
                "rack_no": rack_no,
                "shelf_no": shelf_no,
                "tub_no": tub_no,
                "remark": remark
            }
            serializer = StoreLocationSerializer(
                data=storeloc, context=request)
            if serializer.is_valid():
                print("store loc =>", storeloc)

                serializer.save()
            else:
                print("store loc error => ", serializer.errors)

        # STORE LOCATION
        validated_data.pop('row_no', None)
        validated_data.pop('rack_no', None)
        validated_data.pop('shelf_no', None)
        validated_data.pop('tub_no', None)
        validated_data.pop('remark', None)
        return super().update(instance, validated_data)



class PartsSerializer(serializers.ModelSerializer):
    product_pic_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    specification_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_product_pic = serializers.BooleanField(
        default=False, required=False, write_only=True)
    del_specification = serializers.BooleanField(
        default=False, required=False, write_only=True)
    drawing_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_drawing_pic = serializers.BooleanField(
        default=False, required=False, write_only=True)
    row_no = serializers.CharField(required=False, write_only=True)
    rack_no = serializers.CharField(required=True, write_only=True)
    shelf_no = serializers.CharField(required=False, write_only=True)
    tub_no = serializers.CharField(required=True, write_only=True)
    remark = serializers.CharField(required=False, write_only=True)
    class Meta:
        model = PartsMaster
        field = ['__all__', 'product_pic_upload', 'drawing_upload','del_specification',
                 'del_drawing_pic', 'row_no', 'rack_no', 'shelf_no', 'remark']
        extra_kwargs = {
            "product_pic_url": {
                "required": False
            },
            "product_drawing_no": {
                "required": False

            },
            "modify_date": {
                "required": False

            },
            "modify_by": {
                "required": False

            },
            "aproved_by": {
                "required": False

            },
            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },
            "is_active": {
                "required": False,
                "default": True
            }
        }
        exclude = []

    def validate_product_part_no(self, value):
        part = self.instance  # Get the current assemblies instance being updated
        if part is not None and str(part.product_part_no).strip() == str(value).strip():
            return value  # a_no not changed, no need to perform validation

        if PartsMaster.objects.filter(product_part_no=value).exists():
            raise serializers.ValidationError(
                "This Part no is already in use.")
        return value

    def to_representation(self, instance: PartsMaster):
        representation = super().to_representation(instance)
        product_category = instance.category
        category_name = getattr(product_category, 'c_name', None)
        store_values = StoreLocation.objects.filter(
            part=instance.part_id).values()

        store_data = list(store_values)
        for store_item in store_data:
            representation.update(store_item)
        if StockMaster.objects.filter(part=instance.part_id).exists():
            stock_avail=StockMaster.objects.get(part=instance.part_id)
            
            representation['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
        else:
                            representation['stock_avail'] = 0
        representation['product_category_name'] = category_name

        return representation

    def create(self, validated_data):
        # Retrieve necessary data from validated_data
        request = {"request": self.context['request']}

        product_pic_upload = validated_data.get('product_pic_upload', None)
        drawing_upload = validated_data.get('drawing_upload', None)
        row_no = validated_data.get('row_no', None)
        rack_no = validated_data.get('rack_no', None)
        shelf_no = validated_data.get('shelf_no', None)
        tub_no = validated_data.get('tub_no', None)
        remark = validated_data.get('remark', None)
        product_pic_url = None
        draw_pic_url = None
        print(validated_data)
        # Get the user making the request
        requestuser = self.context['request'].user
        # STORE LOCATION
        validated_data.pop('del_specification',None)
        validated_data.pop('row_no', None)
        validated_data.pop('rack_no', None)
        validated_data.pop('shelf_no', None)
        validated_data.pop('tub_no', None)
        validated_data.pop('remark', None)
        # Set initial values
        validated_data['product_type'] = 1
        validated_data.pop('drawing_upload', None)
        specification_upload=validated_data.pop('specification_upload', None)
        validated_data.pop('del_product_pic', False)
        validated_data.pop('del_drawing_pic', False)
        validated_data.pop('product_pic_upload', None)
        validated_data['create_date'] = timezone.now()
        validated_data['create_by'] = requestuser.id

        # Call the superclass's create method to create a new product instance
        part = super().create(validated_data)
        # part add in  stock

        serializer = Stock_Serializers(data={"part": part.part_id})
        if serializer.is_valid():
            serializer.save()
        else:
            print("stock add error => ", serializer.errors)
        print("part_no ", part.part_id)

        # Handle product picture upload
        if product_pic_upload is not None and len(product_pic_upload) != 0:
            fs = FileSystemStorage()
            product_pic_upload_name = product_pic_upload.name.replace(' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_' +validated_data.get('product_part_no')+product_pic_upload_name}", product_pic_upload)
            else:
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_'+product_pic_upload_name}", product_pic_upload)
            product_pic_url = fs.url(filename)

        # Handle drawing upload
        if drawing_upload is not None and len(drawing_upload) != 0:
            fs = FileSystemStorage()
            drawing_upload_name = drawing_upload.name.replace(' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_'+validated_data.get('product_part_no')+drawing_upload_name}", drawing_upload)
            else:
                filename = fs.save(
                    f"Uploads/Parts/{str(part.part_id)+'_' +drawing_upload_name}")
            draw_pic_url = fs.url(filename)
        if specification_upload is not None and len(specification_upload) != 0:
            fs = FileSystemStorage()
            try:
                specification_upload_name = specification_upload.name.replace(' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(
                        f"Uploads/Parts/{str(part.part_id)+'_'+validated_data.get('product_part_no')+specification_upload_name}", specification_upload)
                else:
                    filename = fs.save(
                        f"Uploads/Parts/{str(part.part_id)+'_' +specification_upload_name}")
                specification_upload_url = fs.url(filename)
                validated_data['specification_upload'] = specification_upload_url
            except Exception as e:
                print("Exception raise=>",e)
        # Update the validated_data dictionary with image URLs
        validated_data['product_pic_url'] = product_pic_url
        validated_data['drawing_img'] = draw_pic_url
        partobj = PartsMaster.objects.get(part_id=part.part_id)
        storeloc = {
            "part": partobj.part_id,
            "row_no": row_no,
            "rack_no": rack_no,
            "shelf_no": shelf_no,
            "tub_no": tub_no,
            "remark": remark
        }
        serializer = StoreLocationSerializer(data=storeloc, context=request)
        if serializer.is_valid():
            print("store loc =>", storeloc)
            serializer.save()
        else:
            print("store loc error =>", serializer.errors)

        partupdate = super().update(partobj, validated_data)
        return partupdate

    def update(self, instance, validated_data):
        product_pic_upload = validated_data.get('product_pic_upload', None)
        del_pic = validated_data.get('del_product_pic', False)
        drawing_upload = validated_data.get('drawing_upload', None)
        del_drawing_pic = validated_data.get('del_drawing_pic', False)
        del_specification = validated_data.get('del_specification', False)
        request = {"request": self.context['request']}
        specification_upload=validated_data.pop('specification_upload', None)
        specification_upload=validated_data.pop('specification_upload', None)

        product_part_no = validated_data.get(
            'product_part_no', instance.product_part_no)
        print(validated_data)
        if del_pic:
            if instance.product_pic_url != None:
                cp = os.getcwd()
                p = str(cp + instance.product_pic_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete product_pic_url img error :", e)
                instance.product_pic_url = None
                instance.save()
        if del_drawing_pic:
            if instance.drawing_img != None:
                cp = os.getcwd()
                p = str(cp + instance.drawing_img)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete drawing_img  error :", e)
                instance.drawing_img = None
                instance.save()
        if del_specification:
            if instance.specification_upload != None:
                cp = os.getcwd()
                p = str(cp + instance.specification_upload)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete drawing_img  error :", e)
                instance.specification_upload = None
                instance.save()
        requestuser = self.context['request'].user

        if product_pic_upload != None:
            if len(product_pic_upload) != 0:
                # delete old product pic url
                if instance.product_pic_url != None:
                    cp = os.getcwd()
                    p = str(cp + instance.product_pic_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete product part img error :", e)

                fs = FileSystemStorage()
                product_pic_upload_name = product_pic_upload.name.replace(
                    ' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id)+'_'+validated_data.get('product_part_no')+product_pic_upload_name}",
                                       product_pic_upload)
                else:

                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id) +'_'+ instance.product_part_no}",
                                       product_pic_upload)

                product_pic_url = fs.url(filename)
                validated_data['product_pic_url'] = product_pic_url
        
        if drawing_upload != None:
            if len(drawing_upload) != 0:
                if instance.drawing_img != None:
                    cp = os.getcwd()
                    p = str(cp + instance.drawing_img)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete drawing_img img error :", e)

                fs = FileSystemStorage()
                drawing_img_name = drawing_upload.name
                drawing_img_name = drawing_img_name.replace(' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id)+'_' +validated_data.get('product_part_no')+drawing_img_name}",
                                       drawing_upload)
                else:
                    filename = fs.save(f"Uploads/Parts/{str(instance.part_id)+'_' +instance.product_part_no+drawing_img_name}",
                                       drawing_upload)

                draw_img_url = fs.url(filename)
                validated_data['drawing_img'] = draw_img_url

        if specification_upload is not None and len(specification_upload) != 0:
            fs = FileSystemStorage()
            if instance.specification_upload != None:
                    cp = os.getcwd()
                    p = str(cp + instance.specification_upload)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete drawing_img img error :", e)

            try:
                specification_upload_name = specification_upload.name.replace(' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(
                        f"Uploads/Parts/{str(instance.part_id)+'_'+validated_data.get('product_part_no')+specification_upload_name}", specification_upload)
                else:
                    filename = fs.save(
                        f"Uploads/Parts/{str(instance.part_id)+'_' +specification_upload_name}")
                specification_upload_url = fs.url(filename)
                validated_data['specification_upload'] = specification_upload_url
                
            except Exception as e:
                print("Exception raise=>",e)
        
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        if validated_data.get('is_active') == False:
            validated_data['closed_by'] = requestuser.id

        del_drawing_pic = validated_data.pop('del_drawing_pic', False)
        drawing_upload = validated_data.pop('drawing_upload', None)
        if StoreLocation.objects.filter(part=instance).exists():
            row_no = validated_data.get('row_no', None)
            rack_no = validated_data.get('rack_no', None)
            shelf_no = validated_data.get('shelf_no', None)
            tub_no = validated_data.get('tub_no', None)
            remark = validated_data.get('remark', None)
            storeinstance = StoreLocation.objects.get(part=instance)
            storeloc = {
                "part": instance.part_id,
                "row_no": row_no,
                "rack_no": rack_no,
                "shelf_no": shelf_no,
                "tub_no": tub_no,
                "remark": remark
            }
            serializer = StoreLocationSerializer(
                instance=storeinstance, data=storeloc, context=request)
            if serializer.is_valid():
                print("store loc =>", storeloc)
                serializer.save()
            else:
                print("store loc error => ", serializer.errors)
        else:
            row_no = validated_data.get('row_no', None)
            rack_no = validated_data.get('rack_no', None)
            shelf_no = validated_data.get('shelf_no', None)
            tub_no = validated_data.get('tub_no', None)
            remark = validated_data.get('remark', None)

            storeloc = {
                "part": instance.part_id,
                "row_no": row_no,
                "rack_no": rack_no,
                "shelf_no": shelf_no,
                "tub_no": tub_no,
                "remark": remark
            }
            serializer = StoreLocationSerializer(
                data=storeloc, context=request)
            if serializer.is_valid():
                print("store loc =>", storeloc)

                serializer.save()
            else:
                print("store loc error => ", serializer.errors)

        # STORE LOCATION
        validated_data.pop('row_no', None)
        validated_data.pop('rack_no', None)
        validated_data.pop('shelf_no', None)
        validated_data.pop('tub_no', None)
        validated_data.pop('remark', None)
        return super().update(instance, validated_data)




class SubPartSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubpartMaster
        extra_kwargs = {

            "create_date": {
                "required": False,
                
            },
            "create_by": {
                "required": False
            },
            "modify_date": {
                "default":timezone.now()
            },
           

        }
        exclude = []

    def create(self, validated_data):
        print("create validated_data => ", validated_data)
        requestuser = self.context['request'].user
        validated_data['create_date'] = timezone.now()
        validated_data['created_by'] = requestuser.id
        return super().create(validated_data)

    def update(self, instance, validated_data):
        print("update subpart => ", validated_data)
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date']=timezone.now()
        #  print('instance => ',instance)
        return super().update(instance, validated_data)


def handle_subpart_list(subpart_list, exclude_fields):
    result_data = []
    for part_obj in subpart_list:
        part_instance = PartsMaster.objects.get(
            part_id=part_obj['sub_part_id'])
        # Serialize the PartsMaster instance
        part_serializer = PartsSerializer(part_instance)
        part_data = part_serializer.data

        for field in exclude_fields:
            part_data.pop(field, None)
            part_obj.pop(field, None)

        merged_data = {**part_obj, **part_data}  # Merge the dictionaries
        result_data.append(merged_data)
        # print('merged data',result_data)
    return result_data


class AssemblySerializer(serializers.ModelSerializer):
    assembly_pic_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_assembly_pic = serializers.BooleanField(
        default=False, required=False, write_only=True)
    part_list = serializers.CharField(required=True, write_only=True)
    sub_assembly_list = serializers.CharField(required=True, write_only=True)
    row_no = serializers.CharField(required=False, write_only=True)
    rack_no = serializers.CharField(required=False, write_only=True)
    shelf_no = serializers.CharField(required=False, write_only=True)
    tub_no = serializers.CharField(required=False, write_only=True)
    remark = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = PartsMaster
        field = ['__all__', 'assembly_pic_upload', 'del_assembly_pic',
                 'row_no', 'rack_no', 'shelf_no', 'remark']
        extra_kwargs = {

            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },

            "is_active": {
                "required": False,
                "default": True

            }
        }
        exclude = []

    def to_representation(self, instance: PartsMaster):
        data = super().to_representation(instance)
        if instance.part_id:
            exclude_fields = ['modify_by', 'created_by',
                              'create_date', 'modify_date','part_id']

            part_list_obj = SubpartMaster.objects.filter(
                part=instance.part_id, subpart_type=1, subpart_subtype=1).values()
            subassembly_list_obj = SubpartMaster.objects.filter(
                part=instance.part_id, subpart_type=2, subpart_subtype=1).values()

            data['part_list'] = handle_subpart_list(
                part_list_obj, exclude_fields)
            
            data['subassembly_list'] = handle_subpart_list(
                subassembly_list_obj, exclude_fields)
        # print(data,"check")
        return data

    def validate_product_part_no(self, value):
        part = self.instance  # Get the current assemblies instance being updated
        if part is not None and part.product_part_no == value:
            return value  # a_no not changed, no need to perform validation

        if PartsMaster.objects.filter(product_part_no=value).exists():
            raise serializers.ValidationError(
                "This Assembly no is already in use.")
        return value

    def create(self, validated_data):
        assembly_pic_upload = validated_data.get('assembly_pic_upload', None)
        sub_assembly_list = validated_data.get('sub_assembly_list', None)
        part_list = validated_data.get('part_list', None)
        a_image_url = None
        request = {"request": self.context['request']}
        requestuser = self.context['request'].user
        validated_data['product_type'] = 2
        print(validated_data)

        row_no = validated_data.get('row_no', None)
        rack_no = validated_data.get('rack_no', None)
        shelf_no = validated_data.get('shelf_no', None)
        tub_no = validated_data.get('tub_no', None)
        remark = validated_data.get('remark', None)

        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()
        validated_data.pop('del_assembly_pic', False)
        validated_data.pop('assembly_pic_upload', None)
        validated_data.pop('part_list', None)
        validated_data.pop('sub_assembly_list', None)

        # STORE LOCATION
        validated_data.pop('row_no', None)
        validated_data.pop('rack_no', None)
        validated_data.pop('shelf_no', None)
        validated_data.pop('tub_no', None)
        validated_data.pop('remark', None)

        assembly = super().create(validated_data)
        assemblyobj = PartsMaster.objects.get(part_id=assembly.part_id)
        # assembly add in  stock
        serializer = Stock_Serializers(data={"part": assembly.part_id})
        if serializer.is_valid():
            serializer.save()
        else:
            print("stock add error => ", serializer.errors)
        print(assembly.product_type, "check project type")
        if part_list is not None:
            try:
                decoded_part_list = json.loads(part_list)
                if len(decoded_part_list) != 0:
                    for part in decoded_part_list:

                        part['part'] = assemblyobj.part_id
                        part['subpart_type'] = 1
                        part['subpart_subtype'] = 1
                        part['part_is_active'] = True
                        serializer = SubPartSerializer(
                            data=part, context=request)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)
                        # print("part_list",serializer)
            except json.JSONDecodeError as e:
                print("partlist json: ", e)
        if sub_assembly_list is not None:
            try:
                decodedsub_assembly_list = json.loads(sub_assembly_list)
                if len(decodedsub_assembly_list) != 0:
                    for subassembly in decodedsub_assembly_list:
                        subassembly['part'] = assemblyobj.part_id
                        subassembly['subpart_type'] = 2
                        subassembly['subpart_subtype'] = 1
                        subassembly['part_is_active'] = True
                        serializer = SubPartSerializer(
                            data=subassembly, context=request)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

            except json.JSONDecodeError as e:
                print("subassembly json: ", e)

        # Handle product picture upload
        if assembly_pic_upload is not None and len(assembly_pic_upload) != 0:
            fs = FileSystemStorage()
            assembly_pic_upload_name = assembly_pic_upload.name.replace(
                ' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Assembly/{str(assembly.part_id)+'_' +validated_data.get('product_part_no')+assembly_pic_upload_name}", assembly_pic_upload)
            else:
                filename = fs.save(
                    f"Uploads/Assembly/{str(assembly.part_id)+'_'+assembly_pic_upload_name}", assembly_pic_upload)
            a_image_url = fs.url(filename)

        validated_data['product_pic_url'] = a_image_url
        storeloc = {
            "part": assemblyobj.part_id,
            "row_no": row_no,
            "rack_no": rack_no,
            "shelf_no": shelf_no,
            "tub_no": tub_no,
            "remark": remark
        }
        serializer = StoreLocationSerializer(data=storeloc, context=request)
        if serializer.is_valid():
            print("store loc =>", storeloc)
            serializer.save()
        else:
            print("store loc error =>", serializer.errors)

        assemblyupdate = super().update(assemblyobj, validated_data)

        return assemblyupdate

    def update(self, instance, validated_data):
        assembly_pic_upload = validated_data.get('assembly_pic_upload', None)
        sub_assembly_list = validated_data.get('sub_assembly_list', None)
        part_list = validated_data.get('part_list', None)
        del_pic = validated_data.get('del_assembly_pic', False)
        validated_data.pop('assembly_pic_upload', None)
        parterror = []
        sub_assemblyerror = []
        request = {"request": self.context['request']}
        if del_pic:
            if instance.product_pic_url != None:
                cp = os.getcwd()
                p = str(cp + instance.product_pic_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except FileNotFoundError as e:
                    print(f"File not found at {p}. Error: {e}")
                except Exception as e:
                    print("delete assembly img error :", e)
                instance.product_pic_url = None
                instance.save()
        requestuser = self.context['request'].user
        if assembly_pic_upload != None:
            if len(assembly_pic_upload) != 0:
                if instance.product_pic_url != None:
                    cp = os.getcwd()
                    p = str(cp + instance.product_pic_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except FileNotFoundError as e:
                        print(f"File not found at {p}. Error: {e}")
                    except Exception as e:
                        print("delete profile img error :", e)

                fs = FileSystemStorage()

                assembly_pic_upload_name = assembly_pic_upload.name.replace(
                    ' ', '_')
                if validated_data.get('product_part_no'):
                    filename = fs.save(
                        f"Uploads/Assembly/{str(instance.part_id)+'_' +validated_data.get('product_part_no')+assembly_pic_upload_name}", assembly_pic_upload)
                else:
                    filename = fs.save(
                        f"Uploads/Assembly/{str(instance.part_id)+'_'+assembly_pic_upload_name}", assembly_pic_upload)
                a_image_url = fs.url(filename)
                validated_data['product_pic_url'] = a_image_url

        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()

        if validated_data.get('is_active') == False:
            validated_data['closed_by'] = requestuser.id

        del_assembly_pic = validated_data.pop('del_assembly_pic', False)
        validated_data.pop('part_list', None)
        validated_data.pop('sub_assembly_list', None)
        if part_list is not None:
            try:
                decoded_part_list = json.loads(part_list)
                if len(decoded_part_list) != 0:
                    for part in decoded_part_list:
                        print("part => ", SubpartMaster.objects.filter(part=instance.part_id, sub_part=part.get(
                            'sub_part'), subpart_type=1, subpart_subtype=1).exists())
                        if SubpartMaster.objects.filter(part=instance.part_id, sub_part=part.get('sub_part'), subpart_type=1, subpart_subtype=1).exists():
                            subinstance = SubpartMaster.objects.get(
                                subpart_master_id=part['subpart_master_id'])
                            part['part'] = instance.part_id
                            part['subpart_type'] = 1
                            part['subpart_subtype'] = 1
                            part['part_is_active'] = True

                            serializer = SubPartSerializer(
                                instance=subinstance, data=part, context=request)
                            print("update part list")

                            if serializer.is_valid():
                                serializer.save()
                            else:
                                parterror.append(serializer.errors)
                                print(serializer.errors)
                        else:
                            print("add part list")
                            part['part'] = instance.part_id
                            part['subpart_type'] = 1
                            part['subpart_subtype'] = 1
                            part['part_is_active'] = True
                            serializer = SubPartSerializer(
                                data=part, context=request)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                parterror.append(serializer.errors)
                                print(serializer.errors)
                        print("part_list", serializer)
            except json.JSONDecodeError as e:
                print("partlist json: ", e)
        if sub_assembly_list is not None:
            try:
                decodedsub_assembly_list = json.loads(sub_assembly_list)
                if len(decodedsub_assembly_list) != 0:

                    for subassembly in decodedsub_assembly_list:
                        print("assem ", SubpartMaster.objects.filter(part=instance.part_id, sub_part=subassembly.get(
                            'sub_part'), subpart_type=2, subpart_subtype=1).exists(), subassembly)
                        if SubpartMaster.objects.filter(part=instance.part_id, sub_part=subassembly.get('sub_part'), subpart_type=2, subpart_subtype=1).exists():
                            subinstance = SubpartMaster.objects.get(
                                subpart_master_id=subassembly['subpart_master_id'])
                            subassembly['part'] = instance.part_id
                            subassembly['subpart_type'] = 2
                            subassembly['subpart_subtype'] = 1
                            subassembly['part_is_active'] = True
                            serializer = SubPartSerializer(
                                instance=subinstance, data=subassembly, context=request)
                            print("update assemm list")

                            if serializer.is_valid():
                                serializer.save()
                            else:
                                sub_assemblyerror.append(serializer.errors)
                                print(serializer.errors)
                        else:

                            subassembly['part'] = instance.part_id
                            subassembly['subpart_type'] = 2
                            subassembly['subpart_subtype'] = 1
                            subassembly['part_is_active'] = True
                            print("add assemm list")

                            serializer = SubPartSerializer(
                                data=subassembly, context=request)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                sub_assemblyerror.append(serializer.errors)
                                print(serializer.errors)

            except json.JSONDecodeError as e:
                print("subassembly json: ", e)

            if StoreLocation.objects.filter(part=instance).exists():
                row_no = validated_data.get('row_no', None)
                rack_no = validated_data.get('rack_no', None)
                shelf_no = validated_data.get('shelf_no', None)
                tub_no = validated_data.get('tub_no', None)
                remark = validated_data.get('remark', None)
                storeinstance = StoreLocation.objects.get(part=instance)
                storeloc = {
                    "part": instance.part_id,
                    "row_no": row_no,
                    "rack_no": rack_no,
                    "shelf_no": shelf_no,
                    "tub_no": tub_no,
                    "remark": remark
                }
                serializer = StoreLocationSerializer(
                    instance=storeinstance, data=storeloc, context=request)
                if serializer.is_valid():
                    print("store loc =>", storeloc)
                    serializer.save()
                else:
                    print("store loc error => ", serializer.errors)
        else:
            row_no = validated_data.get('row_no', None)
            rack_no = validated_data.get('rack_no', None)
            shelf_no = validated_data.get('shelf_no', None)
            tub_no = validated_data.get('tub_no', None)
            remark = validated_data.get('remark', None)

            storeloc = {
                "part": instance.part_id,
                "row_no": row_no,
                "rack_no": rack_no,
                "shelf_no": shelf_no,
                "tub_no": tub_no,
                "remark": remark
            }
            serializer = StoreLocationSerializer(
                data=storeloc, context=request)
            if serializer.is_valid():
                print("store loc =>", storeloc)

                serializer.save()
            else:
                print("store loc error => ", serializer.errors)

        # STORE LOCATION
        validated_data.pop('row_no', None)
        validated_data.pop('rack_no', None)
        validated_data.pop('shelf_no', None)
        validated_data.pop('tub_no', None)
        validated_data.pop('remark', None)
        data = super().update(instance, validated_data)

        response_data = {'data': data, 'partlist_error': parterror,
                         'subassembly_error': sub_assemblyerror}
        print(response_data)
        return data


class MachineSerializer(serializers.ModelSerializer):
    machine_pic_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_machine_pic = serializers.BooleanField(
        default=False, required=False, write_only=True)
    part_list = serializers.CharField(required=True, write_only=True)
    assembly_list = serializers.CharField(required=True, write_only=True)
    standard_accessories_list = serializers.CharField(
        required=True, write_only=True)
    optional_accessories_list = serializers.CharField(
        required=True, write_only=True)

    class Meta:
        model = PartsMaster
        field = ['__all__', 'assembly_pic_upload', 'del_machine_pic',]
        extra_kwargs = {

            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },

            "is_active": {
                "required": False,
                "default": True

            }
        }
        exclude = []

    def to_representation(self, instance: PartsMaster):
        data = super().to_representation(instance)
        if instance.part_id:

            part_list_obj = SubpartMaster.objects.filter(
                Q(part=instance) & Q(subpart_subtype=1) & Q(subpart_type=1)).values()
            assembly_list_obj = SubpartMaster.objects.filter(
                Q(part=instance) & Q(subpart_subtype=1) & Q(subpart_type=2)).values()
            standard_assembly_list_obj = SubpartMaster.objects.filter(
                Q(part=instance) & Q(subpart_subtype=2) & Q(subpart_type__in=[1, 2])).values()
            optional_assembly_list_obj = SubpartMaster.objects.filter(
                Q(part=instance) & Q(subpart_subtype=3) & Q(subpart_type__in=[1, 2])).values()

            exclude_fields = ['modify_by', 'created_by',
                              'create_date', 'modify_date']

            data['part_list'] = handle_subpart_list(
                part_list_obj, exclude_fields)

            data['assembly_list'] = handle_subpart_list(
                assembly_list_obj, exclude_fields)
            data['standard_accessories_list'] = handle_subpart_list(
                standard_assembly_list_obj, exclude_fields)
            data['optional_accessories_list'] = handle_subpart_list(
                optional_assembly_list_obj, exclude_fields)

        return data

    def validate_product_part_no(self, value):
        part = self.instance  # Get the current assemblies instance being updated
        if part is not None and part.product_part_no == value:
            return value  # a_no not changed, no need to perform validation

        if PartsMaster.objects.filter(product_part_no=value).exists():
            raise serializers.ValidationError(
                "This Machine no is already in use.")
        return value

    def create(self, validated_data):
        machine_pic_upload = validated_data.get('machine_pic_upload', None)
        assembly_list = validated_data.get('assembly_list', None)
        standard_accessories_list = validated_data.get(
            'standard_accessories_list', None)
        optional_accessories_list = validated_data.get(
            'optional_accessories_list', None)
        part_list = validated_data.get('part_list', None)
        a_image_url = None
        request = {"request": self.context['request']}
        requestuser = self.context['request'].user
        validated_data['product_type'] = 3

        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()
        validated_data.pop('del_machine_pic', False)
        validated_data.pop('machine_pic_upload', None)
        validated_data.pop('part_list', None)
        validated_data.pop('assembly_list', None)
        validated_data.pop('standard_accessories_list', None)
        validated_data.pop('optional_accessories_list', None)

        machine = super().create(validated_data)
        machineobj = PartsMaster.objects.get(part_id=machine.part_id)
        print(machine.product_type, "check project type")
        if part_list is not None:
            try:
                decoded_part_list = json.loads(part_list)
                if len(decoded_part_list) != 0:
                    for part in decoded_part_list:

                        part['part'] = machineobj.part_id
                        part['subpart_type'] = 1
                        part['subpart_subtype'] = 1
                        part['part_is_active'] = True
                        serializer = SubPartSerializer(
                            data=part, context=request)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)
                        print("part_list", serializer)
            except json.JSONDecodeError as e:
                print("partlist json: ", e)
        if assembly_list is not None:
            try:
                decodedassembly_list = json.loads(assembly_list)
                if len(decodedassembly_list) != 0:
                    for subassembly in decodedassembly_list:
                        subassembly['part'] = machineobj.part_id
                        subassembly['subpart_type'] = 2
                        subassembly['subpart_subtype'] = 1
                        subassembly['part_is_active'] = True
                        serializer = SubPartSerializer(
                            data=subassembly, context=request)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

            except json.JSONDecodeError as e:
                print("assembly json: ", e)
        if standard_accessories_list is not None:
            try:
                decoded_standard_accessories_list = json.loads(
                    standard_accessories_list)
                if len(decoded_standard_accessories_list) != 0:
                    for accessories in decoded_standard_accessories_list:
                        accessories['part'] = machineobj.part_id

                        accessories['subpart_subtype'] = 2
                        accessories['part_is_active'] = True
                        serializer = SubPartSerializer(
                            data=accessories, context=request)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

            except json.JSONDecodeError as e:
                print("standard assembly json: ", e)
        if optional_accessories_list is not None:
            try:
                decoded_optional_accessories_list = json.loads(
                    optional_accessories_list)
                if len(decoded_optional_accessories_list) != 0:
                    for accessories in decoded_optional_accessories_list:
                        accessories['part'] = machineobj.part_id

                        accessories['subpart_subtype'] = 3
                        accessories['part_is_active'] = True
                        serializer = SubPartSerializer(
                            data=accessories, context=request)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

            except json.JSONDecodeError as e:
                print("standard assembly json: ", e)

        # Handle product picture upload
        if machine_pic_upload is not None and len(machine_pic_upload) != 0:
            fs = FileSystemStorage()
            machine_pic_upload_name = machine_pic_upload.name.replace(' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Machines/{str(machine.part_id)+'_' +validated_data.get('product_part_no')+machine_pic_upload_name}", machine_pic_upload)
            else:
                filename = fs.save(
                    f"Uploads/Machines/{str(machine.part_id)+'_'+machine_pic_upload_name}", machine_pic_upload)
            a_image_url = fs.url(filename)

        validated_data['product_pic_url'] = a_image_url
        machineupdate = super().update(machineobj, validated_data)
        return machineupdate

    def update(self, instance:PartsMaster, validated_data):
        machine_pic_upload = validated_data.get('machine_pic_upload', None)
        assembly_list = validated_data.get('assembly_list', None)
        standard_accessories_list = validated_data.get(
            'standard_accessories_list', None)
        optional_accessories_list = validated_data.get(
            'optional_accessories_list', None)
        part_list = validated_data.get('part_list', None)
        a_image_url = None
        request = {"request": self.context['request']}
        requestuser = self.context['request'].user
        validated_data['product_type'] = 3

        del_machine_pic = validated_data.get('del_machine_pic')
        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()
        validated_data.pop('del_machine_pic', False)
        validated_data.pop('machine_pic_upload', None)
        validated_data.pop('part_list', None)
        validated_data.pop('assembly_list', None)
        validated_data.pop('standard_accessories_list', None)
        validated_data.pop('optional_accessories_list', None)
        
        if del_machine_pic:
            if instance.product_pic_url != None:
                cp = os.getcwd()
                p = str(cp + instance.product_pic_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except FileNotFoundError as e:
                    print(f"File not found at {p}. Error: {e}")
                except Exception as e:
                    print("delete assembly img error :", e)
                instance.product_pic_url = None
                instance.save()

        machineobj = PartsMaster.objects.get(part_id=instance.part_id)
        if part_list is not None:
            try:
                decoded_part_list = json.loads(part_list)
                if len(decoded_part_list) > 0:
                    existing_records = SubpartMaster.objects.filter(
                        Q(part=machineobj) & Q(
                            subpart_type=1) & Q(subpart_subtype=1)
                    )

                    update_subpart_master_id_list = [part.get(
                        'subpart_master_id') for part in decoded_part_list if part.get('subpart_master_id')]
                    add_subpart_master_id_list = [
                        part for part in decoded_part_list if not part.get('subpart_master_id')]

                    existing_records_list = list(
                        existing_records.values_list('subpart_master_id', flat=True))

                    delete_part_list = list(
                        set(existing_records_list) - set(update_subpart_master_id_list))

                    print("update list=>", update_subpart_master_id_list,
                          existing_records_list)
                    print("add list=> ", add_subpart_master_id_list)
                    print("delete list=> ", delete_part_list)

                    for part in decoded_part_list:
                        if part.get('subpart_master_id') in update_subpart_master_id_list:
                            subinstance = SubpartMaster.objects.get(
                                subpart_master_id=part['subpart_master_id'])
                            part['part'] = instance.part_id
                            part['subpart_type'] = 1
                            part['subpart_subtype'] = 1
                            part['part_is_active'] = True

                            serializer = SubPartSerializer(
                                instance=subinstance, data=part, context=request)
                            print("update part list")

                        else:
                            part['part'] = instance.part_id
                            part['subpart_type'] = 1
                            part['subpart_subtype'] = 1
                            part['part_is_active'] = True

                            serializer = SubPartSerializer(
                                data=part, context=request)
                            print("Add part list")

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

                    if delete_part_list:
                        SubpartMaster.objects.filter(
                            subpart_master_id__in=delete_part_list).delete()

            except json.JSONDecodeError as e:
                print("partlist json: ", e)
        if assembly_list is not None:
            try:
                decoded_assembly_list = json.loads(assembly_list)
                if len(decoded_assembly_list) > 0:
                    existing_records = SubpartMaster.objects.filter(
                        Q(part=machineobj) & Q(
                            subpart_type=2) & Q(subpart_subtype=1)
                    )

                    update_subpart_master_id_list = [assembly.get(
                        'subpart_master_id') for assembly in decoded_assembly_list if assembly.get('subpart_master_id')]
                    add_subpart_master_id_list = [
                        assembly for assembly in decoded_assembly_list if not assembly.get('subpart_master_id')]

                    existing_records_list = list(
                        existing_records.values_list('subpart_master_id', flat=True))

                    delete_part_list = list(
                        set(existing_records_list) - set(update_subpart_master_id_list))

                    print("update list=>", update_subpart_master_id_list,
                          existing_records_list)
                    print("add list=> ", add_subpart_master_id_list)
                    print("delete list=> ", delete_part_list)

                    for assembly in decoded_assembly_list:
                        if assembly.get('subpart_master_id') in update_subpart_master_id_list:
                            subinstance = SubpartMaster.objects.get(
                                subpart_master_id=assembly['subpart_master_id'])
                            assembly['part'] = instance.part_id
                            assembly['subpart_type'] = 2
                            assembly['subpart_subtype'] = 1
                            assembly['part_is_active'] = True

                            serializer = SubPartSerializer(
                                instance=subinstance, data=assembly, context=request)
                            print("update Assembly list")

                        else:
                            assembly['part'] = instance.part_id
                            assembly['subpart_type'] = 2
                            assembly['subpart_subtype'] = 1
                            assembly['part_is_active'] = True

                            serializer = SubPartSerializer(
                                data=assembly, context=request)
                            print("Add Assembly list")

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

                    if delete_part_list:
                        print("delete assemby")
                        SubpartMaster.objects.filter(
                            subpart_master_id__in=delete_part_list).delete()

            except json.JSONDecodeError as e:
                print("assembly list  json: ", e)
        if standard_accessories_list is not None:
            try:
                decoded_standard_accessories_list = json.loads(
                    standard_accessories_list)
                print(json.dumps(decoded_standard_accessories_list, indent=4))
                if len(decoded_standard_accessories_list) > 0:
                    existing_records = SubpartMaster.objects.filter(
                        Q(part=machineobj) & Q(subpart_subtype=2)
                    )

                    update_subpart_master_id_list = [accessories.get(
                        'subpart_master_id') for accessories in decoded_standard_accessories_list if accessories.get('subpart_master_id')]
                    add_subpart_master_id_list = [
                        accessories for accessories in decoded_standard_accessories_list if not accessories.get('subpart_master_id')]

                    existing_records_list = list(
                        existing_records.values_list('subpart_master_id', flat=True))

                    delete_part_list = list(
                        set(existing_records_list) - set(update_subpart_master_id_list))

                    print("update list=>", update_subpart_master_id_list,
                          existing_records_list)
                    print("add list=> ", add_subpart_master_id_list)
                    print("delete list=> ", delete_part_list)

                    for accessories in decoded_standard_accessories_list:
                        if accessories.get('subpart_master_id') in update_subpart_master_id_list:
                            subinstance = SubpartMaster.objects.get(
                                subpart_master_id=accessories['subpart_master_id'])
                            accessories['part'] = instance.part_id

                            accessories['subpart_subtype'] = 2
                            accessories['part_is_active'] = True

                            serializer = SubPartSerializer(
                                instance=subinstance, data=accessories, context=request)
                            print("update accessories list")

                        else:
                            accessories['part'] = instance.part_id

                            accessories['subpart_subtype'] = 2
                            accessories['part_is_active'] = True

                            serializer = SubPartSerializer(
                                data=accessories, context=request)
                            print("Add accessories list")

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

                    if delete_part_list:
                        print("delete assemby")
                        SubpartMaster.objects.filter(
                            subpart_master_id__in=delete_part_list).delete()

            except json.JSONDecodeError as e:
                print("accessories list  json: ", e)

        if optional_accessories_list is not None:
            try:
                decoded_optional_accessories_list = json.loads(
                    optional_accessories_list)
                if len(decoded_optional_accessories_list) > 0:
                    print(decoded_optional_accessories_list)
                    existing_records = SubpartMaster.objects.filter(
                        Q(part=machineobj) & Q(subpart_subtype=3)
                    )

                    update_subpart_master_id_list = [accessories.get(
                        'subpart_master_id') for accessories in decoded_optional_accessories_list if accessories.get('subpart_master_id')]
                    add_subpart_master_id_list = [
                        accessories for accessories in decoded_optional_accessories_list if not accessories.get('subpart_master_id')]

                    existing_records_list = list(
                        existing_records.values_list('subpart_master_id', flat=True))

                    delete_part_list = list(
                        set(existing_records_list) - set(update_subpart_master_id_list))

                    print("update list=>", update_subpart_master_id_list)
                    print("add list=> ", add_subpart_master_id_list)
                    print("delete list=> ", delete_part_list)

                    for accessories in decoded_optional_accessories_list:
                        if accessories.get('subpart_master_id') in update_subpart_master_id_list:
                            subinstance = SubpartMaster.objects.get(
                                subpart_master_id=accessories['subpart_master_id'])
                            accessories['part'] = instance.part_id

                            accessories['subpart_subtype'] = 3
                            accessories['part_is_active'] = True

                            serializer = SubPartSerializer(
                                instance=subinstance, data=accessories, context=request)
                            print("update op accessories list")

                        else:
                            accessories['part'] = instance.part_id

                            accessories['subpart_subtype'] = 3
                            accessories['part_is_active'] = True

                            serializer = SubPartSerializer(
                                data=accessories, context=request)
                            print("Add op accessories list")

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

                    if delete_part_list:
                        print("delete op accessories")
                        SubpartMaster.objects.filter(
                            subpart_master_id__in=delete_part_list).delete()

            except json.JSONDecodeError as e:
                print("op accessories list  json: ", e)

        # Handle product picture upload
        if machine_pic_upload is not None and len(machine_pic_upload) != 0:
            fs = FileSystemStorage()
            machine_pic_upload_name = machine_pic_upload.name.replace(' ', '_')
            if validated_data.get('product_part_no'):
                filename = fs.save(
                    f"Uploads/Machines/{str(machineobj.part_id)+'_' +validated_data.get('product_part_no')+machine_pic_upload_name}", machine_pic_upload)
            else:
                filename = fs.save(
                    f"Uploads/Machines/{str(machineobj.part_id)+'_'+machine_pic_upload_name}", machine_pic_upload)
            a_image_url = fs.url(filename)
            validated_data['product_pic_url'] = a_image_url

        # print(validated_data,a_image_url)

        return super().update(instance, validated_data)


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SourceMaster
        exclude = []

        extra_kwargs = {

            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },

            "is_active": {
                "required": False,

            }
        }

    def validate_s_name(self, value):
        source = self.instance  # Get the current assemblies instance being updated
        if source is not None and source.s_name == value:
            return value  # a_no not changed, no need to perform validation

        if SourceMaster.objects.filter(s_name=value).exists():
            raise serializers.ValidationError(
                "This Source name is already in use.")
        return value

    def create(self, validated_data):
        requestuser = self.context['request'].user
        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()
        validated_data['is_active'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        if validated_data.get('is_active') == False:
            validated_data['closed_by'] = requestuser.id

        return super().update(instance, validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryMaster
        exclude = []
        extra_kwargs = {

            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },

            "is_active": {
                "required": False,

            }
        }

    def validate_c_name(self, value):
        category = self.instance  # Get the current assemblies instance being updated
        if category is not None and category.c_name == value:
            return value  # a_no not changed, no need to perform validation

        if CategoryMaster.objects.filter(c_name=value).exists():
            raise serializers.ValidationError(
                "This Category name is already in use.")
        return value

    def create(self, validated_data):
        requestuser = self.context['request'].user
        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()
        validated_data['is_active'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        if validated_data.get('is_active') == False:
            validated_data['closed_by'] = requestuser.id

        return super().update(instance, validated_data)


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorsMaster
        exclude = []
        extra_kwargs = {

            "create_date": {
                "required": False

            },
            "create_by": {
                "required": False
            },
            "vendor_mobile2":{
                 "required": False,
                 "allow_null": True
            },
            "vendor_mobile3":{
                 "required": False,
                 "allow_null": True
            },
            "is_active": {
                "required": False,

            }
        }
 
    def create(self, validated_data):
        requestuser = self.context['request'].user
        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()
        validated_data['is_active'] = True
        return super().create(validated_data)

    def update(self, instance, validated_data):
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        if validated_data.get('is_active') == False:
            validated_data['closed_by'] = requestuser.id

        return super().update(instance, validated_data)


class PartsVendorsSerializer(serializers.ModelSerializer):
    part_vendor_datasheet_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    del_datasheet = serializers.BooleanField(
        default=False, required=False, write_only=True)
    del_catalog = serializers.BooleanField(
        default=False, required=False, write_only=True)     
    del_quotation = serializers.BooleanField(
        default=False, required=False, write_only=True)
    catalog_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    quotation_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)

    class Meta:
        model = PartsVendorsMaster
        exclude = []
        extra_kwargs = {

            "create_date": {
                "required": False,

            },
            "create_by": {
                "required": False
            },

            "is_active": {
                "required": False,
                "default":True
            }
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['vendor_name'] = instance.vendor.vendor_name
        data['product_part_no'] = instance.part.product_part_no
        # print(instance.part.product_part_no,"*****************")
        # print(data)
        return data

    def create(self, validated_data):
        part_vendor_datasheet_upload = validated_data.get(
            'part_vendor_datasheet_upload', None)
        quotation_upload = validated_data.get('quotation_upload', None)
        catalog_upload = validated_data.get('catalog_upload', None)
        part_vendor_datasheet_url = None
        print(validated_data)
        if part_vendor_datasheet_upload != None:
            if len(part_vendor_datasheet_upload) != 0:
                fs = FileSystemStorage()
                part_vendor_datasheet_upload_name = part_vendor_datasheet_upload.name
                part_vendor_datasheet_upload_name = part_vendor_datasheet_upload_name.replace(
                    ' ', '_')

                if validated_data.get('vendor'):
                    filename = fs.save('Uploads/Parts/datasheet_' + str(validated_data.get('vendor').vendor_id)+"_" + part_vendor_datasheet_upload_name,
                                       part_vendor_datasheet_upload)
                else:
                    filename = fs.save('Uploads/Parts/datasheet_' + part_vendor_datasheet_upload_name,
                                       part_vendor_datasheet_upload)

                part_vendor_datasheet_url = fs.url(filename)
            # del validated_data['product_pic_upload']
            machine_pic_upload = validated_data.pop(
                'part_vendor_datasheet_upload', None)

        if catalog_upload != None:
            if len(catalog_upload) != 0:
                fs = FileSystemStorage()
                catalog_upload_name = catalog_upload.name
                catalog_upload_name = catalog_upload_name.replace(' ', '_')

                if validated_data.get('vendor'):
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Catalog_"+str(validated_data.get('vendor').vendor_id)+'_' + catalog_upload_name,
                                       catalog_upload)
                else:
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Catalog_"+str(validated_data.get('part').part_id)+'_' + catalog_upload_name,
                                       catalog_upload)

                catalog_url = fs.url(filename)
            validated_data['catalog_url'] = catalog_url

            # del validated_data['product_pic_upload']

        validated_data.pop('catalog_upload', None)
        if quotation_upload != None:
            if len(quotation_upload) != 0:
                fs = FileSystemStorage()
                quotation_upload_name = quotation_upload.name
                quotation_upload_name = quotation_upload_name.replace(' ', '_')

                if validated_data.get('vendor'):
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Quatation_"+str(validated_data.get('vendor').vendor_id)+'_' + quotation_upload_name,
                                       quotation_upload)
                else:
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Quatation_"+str(validated_data.get('part').part_id)+'_' + quotation_upload_name,
                                       quotation_upload)

                quatation_url = fs.url(filename)
            # del validated_data['product_pic_upload']
                validated_data['quotation_url'] = quatation_url

        validated_data.pop('quotation_upload', None)
        validated_data['part_vendor_datasheet_url'] = part_vendor_datasheet_url

        del validated_data['del_datasheet']
        del validated_data['del_catalog']
        del validated_data['del_quotation']

        requestuser = self.context['request'].user

        validated_data['is_active'] = True
        print(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        part_vendor_datasheet_upload = validated_data.get(
            'part_vendor_datasheet_upload', None)
        del_datasheet = validated_data.get('del_datasheet', False)
        quotation_upload = validated_data.get('quotation_upload', None)
        catalog_upload = validated_data.get('catalog_upload', None)
        del_catalog = validated_data.get('del_catalog', False)
        del_quatation = validated_data.get('del_quotation', False)
        # print(quotation_upload,"@@@@@@@@@@@")
        if del_datasheet:
            if instance.part_vendor_datasheet_url != None:
                cp = os.getcwd()
                p = str(cp + instance.part_vendor_datasheet_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete datasheet img error :", e)
                instance.part_vendor_datasheet_url = None
                instance.save()
        if del_quatation:
            if instance.quotation_url != None:
                cp = os.getcwd()
                p = str(cp + instance.quotation_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete quotation_url img error :", e)
                instance.quotation_url = None
                instance.save()
        if del_catalog:
            if instance.catalog_url != None:
                cp = os.getcwd()
                p = str(cp + instance.catalog_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                # print(p)
                try:
                    os.remove(p)
                except Exception as e:
                    print("delete catalog_url img error :", e)
                instance.catalog_url = None
                instance.save()
        requestuser = self.context['request'].user
        if catalog_upload != None:
            if len(catalog_upload) != 0:
                if instance.catalog_url != None:
                    cp = os.getcwd()
                    p = str(cp + instance.catalog_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete catalog_url error :", e)
                fs = FileSystemStorage()
                catalog_upload_name = catalog_upload.name
                catalog_upload_name = catalog_upload_name.replace(' ', '_')

                if validated_data.get('vendor'):
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Catalog_"+str(validated_data.get('vendor').vendor_id)+'_' + catalog_upload_name,
                                       catalog_upload)
                else:
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Catalog_"+str(validated_data.get('part').part_id)+'_' + catalog_upload_name,
                                       catalog_upload)

                catalog_url = fs.url(filename)
                validated_data['catalog_url'] = catalog_url

            # del validated_data['product_pic_upload']

        validated_data.pop('catalog_upload', None)
        if quotation_upload != None:
            
            if len(quotation_upload) != 0:
                if instance.quotation_url != None:
                    # print(instance.quotation_url,"**************")
                    cp = os.getcwd()
                    p = str(cp + instance.quotation_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete quotation_url error :", e)
                fs = FileSystemStorage()
                quotation_upload_name = quotation_upload.name
                quotation_upload_name = quotation_upload_name.replace(' ', '_')

                if validated_data.get('vendor'):
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Quatation_"+str(validated_data.get('vendor').vendor_id)+'_' + quotation_upload_name,
                                       quotation_upload)
                else:
                    filename = fs.save('Uploads/Parts/' + "PartVendor_Quatation_"+str(validated_data.get('part').part_id)+'_' + quotation_upload_name,
                                       quotation_upload)

                quatation_url = fs.url(filename)
               
                validated_data['quotation_url'] = quatation_url
        validated_data.pop('quotation_upload', None)

        if part_vendor_datasheet_upload != None:
            if len(part_vendor_datasheet_upload) != 0:
                if instance.part_vendor_datasheet_url != None:
                    cp = os.getcwd()
                    p = str(cp + instance.part_vendor_datasheet_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    # print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete datasheet error :", e)

                fs = FileSystemStorage()
                part_vendor_datasheet_upload_name = part_vendor_datasheet_upload.name
                part_vendor_datasheet_upload_name = part_vendor_datasheet_upload_name.replace(
                    ' ', '_')

                if validated_data.get('vendor'):
                    filename = fs.save('Uploads/Parts/datasheet_' + str(validated_data.get('vendor').vendor_id)+"_" + part_vendor_datasheet_upload_name,
                                       part_vendor_datasheet_upload)
                else:
                    filename = fs.save('Uploads/Parts/datasheet_' + part_vendor_datasheet_upload_name,
                                       part_vendor_datasheet_upload)

                part_vendor_datasheet_url = fs.url(filename)
            # del validated_data['product_pic_upload']

                validated_data['part_vendor_datasheet_url'] = part_vendor_datasheet_url
                print(part_vendor_datasheet_url)
        validated_data.pop('part_vendor_datasheet_upload', None)
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        # if validated_data.get('is_active') == False:
        #     validated_data['closed_by'] = requestuser.id

        validated_data.pop('del_datasheet', False)
        validated_data.pop('del_quotation', False)
        validated_data.pop('del_catalog', False)

        return super().update(instance, validated_data)


class PurchDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchDetails
        exclude = []

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class PurchInwardSerializer(serializers.ModelSerializer):
    part_list = serializers.CharField(required=False, write_only=True)
    invoice_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)
    lr_upload = serializers.FileField(
        allow_null=True, required=False, write_only=True)

    class Meta:
        model = PurchMaster
        exclude = []
        extra_kwargs = {
            'created_date': {"required": False, "default": timezone.now()},
            'create_by': {'required': False},
            'mrr_no': {'required': False},
        }

    def to_representation(self, instance: PurchMaster):
        data = super().to_representation(instance)

        data['vendor_name'] = instance.vendor.vendor_name
        part_list = PurchDetails.objects.filter(mat_iw=data['mat_iw_id']).values(
            'pd_id',
            'part',  # Assuming you have a field 'part_id' in PurchDetails
            'ord_qty',
            'recd_qty',
            'rej_qty',
            'unit_rate',
            'disc_amt',
            'gst_per',
            'qc_reqd',
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_cost=F('part__product_cost'),
            product_descp=F('part__product_descp'),
        )
        data['part_list'] = part_list
        return data

    def create(self, validated_data):
        user_request = self.context['request'].user
        validated_data['create_by'] = user_request.id
        invoice_upload = validated_data.get('invoice_upload')
        lr_upload = validated_data.get('lr_upload')
        validated_data.pop('lr_upload', None)
        validated_data.pop('invoice_upload', None)
        partlist = validated_data.get('part_list')
        print(validated_data)
        validated_data['mrr_no'] =0

        validated_data.pop('part_list', None)
        inward = super().create(validated_data)
        inwardobj = PurchMaster.objects.get(mat_iw_id=inward.mat_iw_id)
        validated_data['mrr_no'] = inward.mat_iw_id
        if invoice_upload != None:
            if len(invoice_upload) != 0:
                fs = FileSystemStorage()
                invoice_upload_name = invoice_upload.name
                invoice_upload_name = invoice_upload_name.replace(' ', '_')

                filename = fs.save('Uploads/PurchareInward/'+'Invoice_' + str(
                    inward.mat_iw_id)+'_' + invoice_upload_name, invoice_upload)

                invoice_upload_url = fs.url(filename)

                validated_data['inv_url'] = invoice_upload_url

        if lr_upload != None:
            if len(lr_upload) != 0:
                fs = FileSystemStorage()
                lr_upload_name = lr_upload.name
                lr_upload_name = lr_upload_name.replace(' ', '_')
                filename = fs.save('Uploads/PurchareInward/'+'LR_' + str(
                    inward.mat_iw_id)+'_' + invoice_upload_name, invoice_upload)

                lr_upload_url = fs.url(filename)

                validated_data['lr_url'] = lr_upload_url
        # print(partlist)
        if partlist is not None:
            try:

                decoded_part_list = json.loads(partlist)
                print(decoded_part_list)
                for part in decoded_part_list:
                    order_Qty = part['ord_qty']
                    received_Qty = part['recd_qty']
                    if StockMaster.objects.filter(part=part['part']).exists():
                        stoc= StockMaster.objects.filter(part=part['part'])[0]
                        stoc.stock_avail=stoc.stock_avail+int(received_Qty)
                        stoc.save()
                    rejected_Qty = part['rej_qty']
                    totalQty = int(received_Qty)-int(rejected_Qty)
                    # totalQty=int(order_Qty-(received_Qty-rejected_Qty))
                    rate = float(part['unit_rate'])
                    total_rate = float(rate)*totalQty
                    # discount_per=part['disc_per']
                    discount_per = part['disc_per']
                    discount_value = (float(discount_per) /
                                      100) * float(total_rate)
                    total_rate = total_rate-discount_value
                    part['disc_amt'] = round(discount_value, 2)
                    gst_per = part.get('gst_per')
                    part.pop('disc_per', None)

                    part['mat_iw'] = inward.mat_iw_id
                    print("part=>", part)
                    serializer = PurchDetailSerializer(data=part)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(serializer.errors)

            except json.JSONDecodeError as e:
                print("partlist json: ", e)

        return super().update(inwardobj, validated_data)


class ShopfloorDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopFloorDetails
        exclude = []

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
# jay code 
class ShopfloorSerializer(serializers.ModelSerializer):
    part_list = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = ShopFloorMaster
        exclude = []
        extra_kwargs = {
            'created_date': {"required": False, "default": timezone.now()},
            'create_by': {'required': False},
        }
    def to_representation(self, instance: ShopFloorMaster):
        data = super().to_representation(instance)
        if instance.from_department:
            data['from_department_name'] = instance.from_department.dept_name
        
        users = AuthUser.objects.filter(id__in=[data['prepared_by'], data['issued_by'], data['auth_by']])
        user_mapping = {user.id: user.username for user in users}

        data['prepared_by_name'] = user_mapping.get(data['prepared_by'])
        data['issued_by_name'] = user_mapping.get(data['issued_by'])
        data['auth_by_name'] = user_mapping.get(data['auth_by'])

        part_list = ShopFloorDetails.objects.filter(mat_sf=data['mat_sf_id']).values(
            'sfd_id',
            'part',  # Assuming you have a field 'part_id' in PurchDetails
            'rtn_qty',
            'ref_no',
            'uom',
            'ioa_no',
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_cost=F('part__product_cost'),
            product_descp=F('part__product_descp'),
        )
        data['part_list'] = part_list
        return data

    def create(self, validated_data):
        user_request = self.context['request'].user
        validated_data['create_by'] = user_request.id
        issued_by = validated_data.get('issued_by')
        shopfloor_count=ShopFloorMaster.objects.all().count()
        formatted_rts_no = 'RTS{:04d}'.format(shopfloor_count+1)
        validated_data['rts_no']=formatted_rts_no
        partlist = validated_data.get('part_list')

        print(validated_data)
        validated_data['status']="RTS_UNDER_APPROVAL"
        validated_data.pop('part_list', None)
        shopfloor = super().create(validated_data)

        shopfloorobj = ShopFloorMaster.objects.get(
            mat_sf_id=shopfloor.mat_sf_id)
        # validated_data['min_no']=shopfloor.mat_sf_id

        print(partlist)
        if partlist is not None:
            try:
                decoded_part_list = json.loads(partlist)
                print(decoded_part_list)
                for part in decoded_part_list:
                    part['mat_sf'] = shopfloorobj.mat_sf_id
                    print("part=>", part)
                    serializer = ShopfloorDetailSerializer(data=part)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        print(serializer.errors)
                notification_message = f"A material return to store with the code {formatted_rts_no} has been generated. Please click here to approve the Part."  


                notification_user = AuthUser.objects.get(pk=issued_by)
                notification = Notification.objects.create(
                        type='RTS_Approval',
                        message=notification_message,
                        created_date=timezone.now(),
                        sender_user_id=user_request.id,
                        receiver_user=notification_user,
                        action=shopfloor.mat_sf_id,
                        is_read=False
                    )
            except json.JSONDecodeError as e:
                print("partlist json: ", e)

        return super().update(shopfloorobj, validated_data)
# om code 
# class ShopfloorSerializer(serializers.ModelSerializer):
#     part_list = serializers.CharField(required=False, write_only=True)

#     class Meta:
#         model = ShopFloorMaster
#         exclude = []
#         extra_kwargs = {
#             'created_date': {"required": False, "default": timezone.now()},
#             'create_by': {'required': False},
#         }

#     def to_representation(self, instance: ShopFloorMaster):
#         data = super().to_representation(instance)
#         if instance.from_department:
#             data['from_department_name']=instance.from_department.dept_name
#         part_list = ShopFloorDetails.objects.filter(mat_sf=data['mat_sf_id']).values(
#             'sfd_id',
#             'part',  # Assuming you have a field 'part_id' in PurchDetails
#             'rtn_qty',
#             'ref_no',
#             'uom',
#             'ioa_no',

#             product_part_no=F('part__product_part_no'),
#             product_part_name=F('part__product_part_name'),
#             product_cost=F('part__product_cost'),
#             product_descp=F('part__product_descp'),
#         )
#         data['part_list'] = part_list
#         return data

#     def create(self, validated_data):
#         user_request = self.context['request'].user
#         validated_data['create_by'] = user_request.id

#         partlist = validated_data.get('part_list')
#         print(validated_data)
#         validated_data.pop('part_list', None)
#         shopfloor = super().create(validated_data)
#         shopfloorobj = ShopFloorMaster.objects.get(
#             mat_sf_id=shopfloor.mat_sf_id)
#         # validated_data['min_no']=shopfloor.mat_sf_id

#         print(partlist)
#         if partlist is not None:
#             try:

#                 decoded_part_list = json.loads(partlist)
#                 print(decoded_part_list)
#                 for part in decoded_part_list:
#                     part['mat_sf'] = shopfloorobj.mat_sf_id
#                     print("part=>", part)
#                     serializer = ShopfloorDetailSerializer(data=part)
#                     if serializer.is_valid():
#                         serializer.save()
#                     else:
#                         print(serializer.errors)

#             except json.JSONDecodeError as e:
#                 print("partlist json: ", e)

#         return super().update(shopfloorobj, validated_data)


class ShopfloorApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopFloorMaster
        fields = ['status','remarks']
        extra_kwargs={
           "status":{
               "required":True
           },
             "remarks": {
                "required": True
            }
        }

    def update_notifications_to_read(self, status, user_id, id):
      
        notification=Notification.objects.filter(
            type=status, receiver_user=user_id, action=id
        )
        for notifi in notification:
            notifi.is_read=True
            notifi.save()

    def create_notification(self, type, message, receiver_user, sender_user_id, id):
        Notification.objects.create(
            type=type,
            message=message,
            created_date=timezone.now(),
            receiver_user=receiver_user,
            sender_user_id=sender_user_id,
            action=id,
            is_read=False
        )

    def handle_approval(self, instance:ShopFloorMaster, validated_data, request_user):
        status = validated_data.get('status')
       
        if status in ['RTS_APPROVED', 'RTS_RETURN', 'RTS_REJECTED']:
            self.update_notifications_to_read('RTS_Approval', request_user.id, instance.mat_sf_id)

        if status == 'RTS_APPROVED':
            sfd=ShopFloorDetails.objects.filter(mat_sf=instance.mat_sf_id)
            # avail stock update  
            for sfd_obj in sfd:
                print(sfd_obj)
                stock=StockMaster.objects.filter(part=sfd_obj.part)[0]
                stock.stock_avail=stock.stock_avail+sfd_obj.rtn_qty
                stock.last_update=timezone.now()
                stock.save()
                StockUpdate.objects.create(
                    part=stock.part,
                    tran_type="Update",
                    stock_avail=stock.stock_avail,
                    updt_date=timezone.now(),
                    updt_by=request_user.id,
                    type=1,
                    remarks="Return to store updation in stock available"

                )
        elif status == 'RTS_RETURN':
            self.process_return(instance, request_user, validated_data)
        elif status == 'RTS_REJECTED':
            pass
            notification_message = f"A material return to store  with the code {instance.rts_no} has been rejected."
            notification_user=AuthUser.objects.filter(id=instance.create_by)
            if notification_user.exists():
                self.create_notification("INFO",notification_message,notification_user,request_user.id,instance.mat_sf_id)
        else:
            raise ValidationError({"message": "Invalid status."})
        
    def process_return(self, instance, request_user, validated_data):
        receiver_notification_user = AuthUser.objects.filter(id=instance.create_by).first()
        if not receiver_notification_user:
            raise ValidationError({"message": "Invalid RTS creator."})

        notification_message = f"A material return to store  with the code {instance.rts_no} has been returned. Please click here to update it."
        self.create_notification(
            type='RTS_Return',
            message=notification_message,
            receiver_user=receiver_notification_user,
            sender_user_id=request_user.id,
            id=instance.mat_sf_id
        )

    def update(self, instance, validated_data):
        request_user = self.context['request'].user
       
        self.handle_approval(instance, validated_data, request_user)

        return super().update(instance, validated_data)


class ShopfloorReturnDetailSerializer(serializers.ModelSerializer):
    sfd_id=serializers.IntegerField()
    class Meta:
        model = ShopFloorDetails
        # fields =['mat_sf','sfd_id','part','rtn_qty',]   
        fields ='__all__'   
        extra_kwargs = {
            "mat_sf":{
                "required":True,    
            },
            "part":{
                "required":True,    
            },
            "rtn_qty":{
                "required":True,    
            },
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)



class ShopfloorReturnSerializer(serializers.ModelSerializer):
    part_list = ShopfloorReturnDetailSerializer(many=True, write_only=True)
    del_part_list = serializers.ListField(required=False, write_only=True)
    
    def validate_part_list(self, value):
        if not value:
            raise serializers.ValidationError("Part list cannot be empty.")
        return value
    def update_notifications_to_read(self, status, user_id, id):
        notification=Notification.objects.filter(
            type=status, receiver_user=user_id, action=id
        )
        for notifi in notification:
            notifi.is_read=True
            notifi.save()
    class Meta:
        model = ShopFloorMaster
        fields = ['status', 'remarks', 'part_list','del_part_list']
    def create_notification(self, type, message, receiver_user, sender_user_id, id):
        Notification.objects.create(
            type=type,
            message=message,
            created_date=timezone.now(),
            receiver_user=receiver_user,
            sender_user_id=sender_user_id,
            action=id,
            is_read=False
        )
    def update(self, instance, validated_data):
        request_user = self.context['request'].user
        try:
            with transaction.atomic():
                partlist = validated_data.pop('part_list', None)
                del_part_list = validated_data.pop('del_part_list', None)

                if del_part_list:
                    ShopFloorDetails.objects.filter(sfd_id__in=del_part_list).delete()
                print(partlist)
                if partlist:
                    for part in partlist:
                        # print("part ==>",part,)
                        sfd_id = part.get('sfd_id')


                        # print("sfd",sfd_id['353'])
                        if sfd_id:
                            # obj, created = ShopFloorDetails.objects.update_or_create(
                            #     sfd_id=sfd_id,
                            #     defaults={key: part[key] for key in [ 'part', 'rtn_qty', ]}
                            # )
                            ShopFloorDetails.objects.filter(sfd_id=sfd_id).update(
                                rtn_qty=part.get('rtn_qty')
                            )
                        #     print(obj.rtn_qty,created)

                # Handle notifications
                self.update_notifications_to_read("RTS_Return",request_user.id,instance.mat_sf_id)


                receiver_notification_user = AuthUser.objects.filter(id=instance.issued_by).first()
                if not receiver_notification_user:
                    raise ValidationError({"message": "Invalid RTS creator."})

                notification_message = f"A material return to store with the code {instance.rts_no} has been generated. Please click here to approve the Part."

                self.create_notification(
                    type='RTS_Approval',
                    message=notification_message,
                    receiver_user=receiver_notification_user,
                    sender_user_id=request_user.id,
                    id=instance.mat_sf_id
                )
                validated_data['status'] = "RTS_UNDER_APPROVAL"
                return super().update(instance, validated_data)
        except Exception as e:
            print(e)
            raise serializers.ValidationError({"error": "An unexpected error occurred."}) from e

class MrsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = MrsDetails
        exclude = []
        extra_kwargs = {
            "status": {
                'required': False,
                'default': False
            },
        }

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class Mrs_Serializers(serializers.ModelSerializer):
    part_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    partdelete_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    raw_mat_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    raw_matdelete_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    assembly_list = serializers.CharField(required=False, write_only=True, default="[]")
    assembly_delete_list = serializers.CharField(required=False, write_only=True, default="[]")
   
    class Meta:
        model = MrsMaster
        exclude = []
        extra_kwargs = {
            "mrs_no": {
                'required': False
            },
            "from_dept": {
                'required': True
            },
            "status": {
                'required': False,
                'default': False

            },
              "modify_date":{
                "default":timezone.now()
            },
            
        }

    def to_representation(self, instance: MrsMaster):
        data = super().to_representation(instance)
        assembly_list=[]
        if MrsMaster.objects.filter(mrs_no=instance.mrs_no,type=True).exists():
            filterdata=MrsMaster.objects.filter(mrs_no=instance.mrs_no,type=True)
            # print(filterdata,instance.mrs_id)
            for assem in filterdata:

                subparts= MrsDetails.objects.filter(mrs=assem,type="SP").values(
                        'part',  
                        'req_qty',
                        'issue_qty',
                        'mrs_detail_id',
                        'ioa_no',
                        'mrs',
                        'type',
                        product_part_no=F('part__product_part_no'),
                        product_part_name=F('part__product_part_name'),
                        product_cost=F('part__product_cost'),
                        # part_desc=F('part__product_descp'),
                        product_descp=F('part__product_descp'),
                        uom=F('part__uom'),
                )
                for subpart in subparts:
                    if subpart.get('type')=='SP':
                        subpartinstance=SubpartMaster.objects.filter(part=assem.part,sub_part=subpart.get('part')).first()
                        if subpartinstance: 
                            subpart['req_store_qty']= subpart['req_qty']
                            subpart['req_qty']=subpartinstance.sub_part_qty
                        if StockMaster.objects.filter(part=subpart.get('part')).exists():
                            stock_avail=StockMaster.objects.get(part=subpart.get('part'))
                           
                            subpart['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
                        else:
                            subpart['stock_avail'] = 0
                            # print(subpart,subpartinstance.sub_part_qty)
                
                assembly_list.append({
                    "mrs_id":assem.mrs_id,
                    "mrs_no":assem.mrs_no,
                    "ioa_no":assem.ioa_no,
                    "issue_by":assem.issue_by,
                    "part":assem.part.part_id,
                    "product_part_name":assem.part.product_part_name,
                    "product_part_no":assem.part.product_part_no,
                    "product_descp":assem.part.product_descp,
                    "req_qty":assem.req_qty,
                    "subpart":subparts
                })

        data['assembly_list']=assembly_list
       

        part_list = MrsDetails.objects.filter(mrs=instance.mrs_id,type='P').values(
            'part',  
            'req_qty',
            'issue_qty',
            'mrs_detail_id',
            'ioa_no',
            'type',
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_cost=F('part__product_cost'),
            # part_desc=F('part__product_descp'),
            product_descp=F('part__product_descp'),
            uom=F('part__uom'),
        )
        for pl in part_list:
            if StockMaster.objects.filter(part=pl['part']).exists():
                stock_avail=StockMaster.objects.get(part=pl['part'])
                # print(pl['part'],stock_avail.stock_avail)
                pl['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
            else:
                pl['stock_avail'] = 0
        raw_mat_list = MrsDetails.objects.filter(mrs=instance.mrs_id,type='RM').values(
            'req_qty',
            'issue_qty',
            'mrs_detail_id',
            'ioa_no',
            'rm',
            'type',
            rm_mat_name=F('rm__rm_mat_name'),
            rm_mat_code=F('rm__rm_mat_code'),
            rm_mat_desc=F('rm__rm_mat_desc'),

        )
        for rm in raw_mat_list:
           
            if StockMaster.objects.filter(rm=rm.get('rm')).exists():
                stock_avail=StockMaster.objects.get(rm=rm.get('rm'))
                # print(stock_avail.stock_avail)
                rm['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
            else:
                rm['stock_avail'] = 0
        data['from_dept_name'] = instance.from_dept.dept_name if instance.from_dept else None

        data['part_list'] = part_list
        data['raw_mat_list'] = raw_mat_list

        return data
    
    def create(self, validated_data):
        user_request = self.context['request'].user
        validated_data['created_date'] = timezone.now()
        validated_data['create_by'] = user_request.id
        partlist = validated_data.get('part_list',None)
        assemby_list = validated_data.get('assembly_list',None)
     
        raw_mat_list = validated_data.get('raw_mat_list')
        print("data=> ",validated_data)    
        
        validated_data.pop('part_list', None)
        validated_data.pop('assembly_list', None)
        validated_data.pop('assembly_delete_list', None)
        validated_data.pop('raw_mat_list', None)
        validated_data.pop('partdelete_list', None)
        validated_data.pop('raw_matdelete_list', None)
        try:
            l_mrs_id = MrsMaster.objects.latest('mrs_no') 
        except MrsMaster.DoesNotExist:
            l_mrs_id=None
        # print(l_mrs_id.mrs_no)
        new_mrs_id =  1
        latest_mrs_no = l_mrs_id.mrs_no if l_mrs_id else None     
        if latest_mrs_no:  
            # Increment the latest mrs_id by 1
            current_mrs_id = int(latest_mrs_no[3:])
            new_mrs_id = current_mrs_id + 1
         
        formatted_mrs_id = 'MRS{:04d}'.format(new_mrs_id)
        # latest_mrs_id = MrsMaster.objects.all().aggregate(Max('mrs_id'))['mrs_id__max']
        # # Increment the latest mrs_id by 1
        # new_mrs_id = latest_mrs_id + 1 if latest_mrs_id is not None else 1
        # formatted_mrs_id = 'MRS{:04d}'.format(new_mrs_id)
        validated_data['mrs_no'] = formatted_mrs_id
        validated_data['type'] = 0
        # print("data=> ",validated_data)    
        
        mrs = super().create(validated_data)
        mrsObj = MrsMaster.objects.get(mrs_id=mrs.mrs_id)
        
        if assemby_list is not None:
            try:
                decoded_assemby_list = json.loads(assemby_list)
              
                if len(decoded_assemby_list) > 0:
                        for assembly in decoded_assemby_list:
                                print(assembly)
                                part_inst= PartsMaster.objects.get(part_id=assembly.get('part'))
                                mrs_assembly = MrsMaster.objects.create(mrs_no=formatted_mrs_id,
                                                               mrs_date=validated_data.get('mrs_date'),part=part_inst,req_qty=assembly.get('req_qty'),
                                                               from_dept=validated_data.get('from_dept'),prep_by=validated_data.get('prep_by'),auth_by=validated_data.get('auth_by')
                                                               ,issue_by=validated_data.get('issue_by'),ioa_no=assembly.get('ioa_no'),remark=validated_data.get('remark'),
                                                               create_by=user_request.id,created_date=timezone.now(),modify_by=user_request.id,modify_date=timezone.now(),type=1,status=0
                                                               )
                                
                                subpartassem= assembly.get('subpart',[])
                                for subpart in subpartassem:
                                    subpart['mrs'] = mrs_assembly.mrs_id
                                    req_qty= int(assembly.get('req_qty',1))
                                    subpart['part']=subpart['sub_part_id']
                                    subpart['type']='SP'
                                    subpart['req_qty']=subpart['sub_part_qty']*req_qty
                                    serializer = MrsDetailSerializer(data=subpart)
                                    if serializer.is_valid():
                                        serializer.save()
                                    else:
                                        print(serializer.errors)
                          
            except json.JSONDecodeError as e:
                    print("assemby json: ", e)

        if partlist is not None:
                try:
                    decoded_part_list = json.loads(partlist)
                    if len(decoded_part_list) >0:
                            decoded_part_list = json.loads(partlist)
                           
                            for part in decoded_part_list:
                                part['mrs'] = mrsObj.mrs_id
                                part['type']='P'
                                # print("part=>", part)
                                serializer = MrsDetailSerializer(data=part)
                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    print(serializer.errors)
    
                except json.JSONDecodeError as e:
                    print("partlist json: ", e)
        
        if raw_mat_list is not None:
                try:
                    decoded_raw_mat_list = json.loads(raw_mat_list)
                    if len(decoded_raw_mat_list) >0:
                       
                        print("RAW MAT",len(raw_mat_list))
                        print(decoded_raw_mat_list)
                        for rm in decoded_raw_mat_list:
                            rm['mrs'] = mrsObj.mrs_id
                            rm['type']='RM'

                            serializer = MrsDetailSerializer(data=rm)
                            if serializer.is_valid():
                                serializer.save()
                            else:
                                print(serializer.errors)

                except json.JSONDecodeError as e:
                    print("raw_mat_list json: ", e)
        
        
        return super().update(mrsObj, validated_data)

    def update(self, instance: MrsMaster, validated_data):
        user_request = self.context['request'].user
        validated_data['modify_by'] = user_request.id
        partlist = validated_data.get('part_list')
        partdelete_list = validated_data.get('partdelete_list')
        raw_matdelete_list = validated_data.get('raw_matdelete_list')
        raw_mat_list = validated_data.get('raw_mat_list')
        assemby_list = validated_data.get('assembly_list',None)
        assemby_delete_list = validated_data.get('assembly_delete_list',None)
        # print(validated_data)
        # print("partdelete_list", partdelete_list)
        validated_data.pop('assembly_list', None)
        validated_data.pop('assembly_delete_list', None)
        validated_data.pop('part_list', None)
        validated_data.pop('raw_mat_list', None)
        validated_data.pop('partdelete_list', None)
        validated_data.pop('raw_matdelete_list', None)
        
        validated_data['modify_date'] = timezone.now()
        if partdelete_list is not None:
                try:
                    decoded_partdelete_list = json.loads(partdelete_list)
                    if len(decoded_partdelete_list)>0:
                        
                        print("decoded_partdelete_list => ",
                              decoded_partdelete_list)
                        MrsDetails.objects.filter(
                            mrs_detail_id__in=decoded_partdelete_list).delete()

                except json.JSONDecodeError as e:
                    print("delete json: ", e)
       
        if assemby_delete_list is not None:
                try:
                    decoded_assemby_delete_list = json.loads(assemby_delete_list)
                    if len(decoded_assemby_delete_list)>0:
                    
                        print("decoded_assemby_delete_list => ",
                              decoded_assemby_delete_list)
                        MrsMaster.objects.filter(
                            mrs_id__in=decoded_assemby_delete_list).delete()

                except json.JSONDecodeError as e:
                    print("delete json: ", e)
        
        if raw_matdelete_list is not None:
                try:
                    decoded_raw_matdelete_list = json.loads(raw_matdelete_list)
                    if len(decoded_raw_matdelete_list)>0:
                        print("decoded_raw_matdelete_list => ",
                              decoded_raw_matdelete_list)
                        MrsDetails.objects.filter(
                            mrs_detail_id__in=decoded_raw_matdelete_list).delete()

                except json.JSONDecodeError as e:
                    print("delete json: ", e)
        
        
        if partlist is not None:
            try:
                decoded_part_list = json.loads(partlist)
                if len(decoded_part_list) >0:

                    print(decoded_part_list)
                    existing_records = MrsDetails.objects.filter(
                        Q(mrs=instance.mrs_id)
                    )
                    update_part_master_id_list = [part.get(
                        'mrs_detail_id') for part in decoded_part_list if part.get('mrs_detail_id')]
                    add_part_master_id_list = [
                        part for part in decoded_part_list if not part.get('mrs_detail_id')]
                    # existing_records_list = list(existing_records.values_list('mrs_detail_id', flat=True))
                    # delete_part_list = list(set(existing_records_list) - set(update_part_master_id_list))
                    
                    for part in decoded_part_list:
                        if part.get('mrs_detail_id') in update_part_master_id_list:
                            mrdinstance = MrsDetails.objects.get(
                                mrs_detail_id=part['mrs_detail_id'])

                            part['mrs'] = instance.mrs_id
                            part['req_qty'] = int(part.get('req_qty',mrdinstance.req_qty))
                            part['type']='P'
                            
                            serializer = MrsDetailSerializer(
                                instance=mrdinstance, data=part)
                            print("update  part list => ", part)

                        else:

                            part['mrs'] = instance.mrs_id
                            part['req_qty'] = int(part.get('req_qty',1))
                            part['type']='P'

                            serializer = MrsDetailSerializer(data=part)

                            print("Add  part list => ", part)

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

            except json.JSONDecodeError as e:
                print("partlist json: ", e)

        if assemby_list is not None:
            try:
                decoded_assemby_list = json.loads(assemby_list)
                if len(decoded_assemby_list) >0:

                   
                    existing_records = MrsMaster.objects.filter(
                        Q(mrs_id=instance.mrs_id)
                    )
                    update_assembly_master_id_list = [part.get(
                        'mrs_id') for part in decoded_assemby_list if part.get('mrs_id')]
                    add_part_master_id_list = [
                        part for part in decoded_assemby_list if not part.get('mrs_id')]
                    # existing_records_list = list(existing_records.values_list('mrs_detail_id', flat=True))
                    # delete_part_list = list(set(existing_records_list) - set(update_part_master_id_list))
                    print("update_assembly_master_id_list=>",update_assembly_master_id_list)
                    for assembly in decoded_assemby_list:
                        if assembly.get('mrs_id') in update_assembly_master_id_list:
                            mrinstance = MrsMaster.objects.get(mrs_id= assembly.get('mrs_id'),type=1)

                            subpartassem= assembly.get('subpart',[])
                            print(mrinstance,subpartassem) 
                            if mrinstance:
                                     MrsDetails.objects.filter(mrs=mrinstance,type="SP").delete()
                            for subpart in subpartassem:
                                subpart['mrs']=mrinstance.mrs_id
                             
                                subpart['type']='SP'

                                subpartinstance=SubpartMaster.objects.filter(part=mrinstance.part,sub_part=subpart.get('part')).first()
                                req_qty= int(assembly.get('req_qty',1))
                                # print("subpartinstance=>",subpartinstance,mrinstance.part,mrdinstance.part,mrdinstance)
                                if subpartinstance:
                                    subpart['req_qty']=int(subpartinstance.sub_part_qty*req_qty)
                                print("subpart=>",subpart)
                                serializer = MrsDetailSerializer(data=subpart)
                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    print(serializer.errors)
                            assembly['mrs_date']=validated_data.get('mrs_date',mrinstance.mrs_date)
                            assembly['from_dept']=validated_data.get('from_dept',mrinstance.mrs_date)
                            assembly['issue_by']=validated_data.get('issue_by',mrinstance.issue_by)
                            assembly['req_qty']=assembly.get('req_qty',mrinstance.req_qty)
                            assembly['prep_by']=validated_data.get('prep_by',mrinstance.prep_by)
                            assembly['remark']=validated_data.get('remark',mrinstance.remark)
                            assembly['auth_by']=validated_data.get('auth_by',mrinstance.auth_by)
                            assembly['ioa_no']=assembly.get('ioa_no',mrinstance.ioa_no)    
                            assembly.pop('subpart',None)
                            print("assembly =>",assembly)
                            part_instan= PartsMaster.objects.get(part_id=assembly.get('part'))
                            assembly['part']=part_instan
                            super().update(mrinstance, assembly)


                            print("update  assembly list")

                        else:
                            # print(assembly,assembly.get('subpart',[]))
                            part_inst= PartsMaster.objects.get(part_id=assembly.get('part'))

                            # print(part_inst)
                            mrs_assembly = MrsMaster.objects.create(mrs_no=instance.mrs_no,
                                                           mrs_date=validated_data.get('mrs_date',instance.mrs_date),part=part_inst,req_qty=assembly.get('req_qty',1),
                                                           from_dept=validated_data.get('from_dept',instance.from_dept),prep_by=validated_data.get('prep_by',instance.prep_by),auth_by=validated_data.get('auth_by',instance.prep_by)
                                                           ,issue_by=validated_data.get('issue_by',instance.issue_by),ioa_no=assembly.get('ioa_no',instance.ioa_no),remark=validated_data.get('remark',instance.remark),
                                                           create_by=user_request.id,created_date=timezone.now(),modify_by=user_request.id,modify_date=timezone.now(),type=1,status=0
                                                           )
                            
                            subpartassem= assembly.get('subpart',[])
                            for subpart in subpartassem:
                                subpart['mrs'] = mrs_assembly.mrs_id
                                req_qty= int(assembly.get('req_qty',1))
                                
                                subpart['part']=subpart['sub_part_id']

                                subpart['type']='SP'
                                subpartinstance=SubpartMaster.objects.filter(part=assembly.get('part'),sub_part=subpart.get('sub_part_id')).first()
                                if subpartinstance:
                                    subpart['req_qty']=subpartinstance.sub_part_qty*req_qty
                                else:
                                    subpart['req_qty']=subpart['req_qty']*req_qty

                                print("subpart =>",subpart)
                                serializer = MrsDetailSerializer(data=subpart)
                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    print(serializer.errors)
                          

                            print("Add assembly list")

                       

            except json.JSONDecodeError as e:
                print("assemby json: ", e)
        if raw_mat_list is not None:
            try:
                decoded_raw_mat_list = json.loads(raw_mat_list)
                if len(decoded_raw_mat_list) >0:

                    print(decoded_raw_mat_list)
                    existing_records = MrsDetails.objects.filter(
                        Q(mrs=instance.mrs_id)
                    )
                    update_raw_mat_list_list = [rm.get(
                        'mrs_detail_id') for rm in decoded_raw_mat_list if rm.get('mrs_detail_id')]
                    add_raw_mat_list_list = [
                        rm for rm in decoded_raw_mat_list if not rm.get('mrs_detail_id')]
                    # existing_records_list = list(existing_records.values_list('mrs_detail_id', flat=True))
                    # delete_part_list = list(set(existing_records_list) - set(update_part_master_id_list))
                    for rm in decoded_raw_mat_list:
                        if rm.get('mrs_detail_id') in update_raw_mat_list_list:
                            mrdinstance = MrsDetails.objects.get(
                                mrs_detail_id=rm['mrs_detail_id'])
                            rm['req_qty'] = int(rm.get('req_qty',mrdinstance.req_qty))
                            rm['type']='RM'

                            rm['mrs'] = instance.mrs_id

                            serializer = MrsDetailSerializer(instance=mrdinstance, data=rm)
                            print("update  raw_mat list")

                        else:
                            rm['type']='RM'
                            
                            rm['mrs'] = instance.mrs_id
                            rm['req_qty'] = int(rm.get('req_qty',1))

                            serializer = MrsDetailSerializer(data=rm)

                            print("Add  rm list")

                        if serializer.is_valid():
                            serializer.save()
                        else:
                            print(serializer.errors)

            except json.JSONDecodeError as e:
                print("rm json: ", e)
         
      

        return super().update(instance, validated_data)


class Min_Serializers(serializers.ModelSerializer):
    part_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    raw_mat_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    assembly_list = serializers.CharField(
        required=False, write_only=True, default="[]")
    class Meta:
        model = MrsMaster
        exclude = []
        extra_kwargs = {
            "issue_by": {
                'required': True
            },

            "status": {
                'required': False,
                'default': False

            },
             "modify_date":{
                "default":timezone.now()
            }
        }

    def to_representation(self, instance: MrsMaster):
        data = super().to_representation(instance)
        assembly_list=[]
        assem_status=[]
        if MrsMaster.objects.filter(mrs_no=instance.mrs_no,type=True).exists():
            filterdata=MrsMaster.objects.filter(mrs_no=instance.mrs_no,type=True)
            # print(filterdata,instance.mrs_id)
            for assem in filterdata:

                subparts= MrsDetails.objects.filter(mrs=assem,type="SP").values(
                        'part',  
                        'req_qty',
                        'issue_qty',
                        'mrs_detail_id',
                        'ioa_no',
                        'mrs',
                        'type',
                        'status',
                        product_part_no=F('part__product_part_no'),
                        product_part_name=F('part__product_part_name'),
                        product_cost=F('part__product_cost'),
                        # part_desc=F('part__product_descp'),
                        product_descp=F('part__product_descp'),
                        uom=F('part__uom'),
                )
                subpartstatus=[]
                for subpart in subparts:
                    if subpart.get('type')=='SP':
                        subpartinstance=SubpartMaster.objects.filter(part=assem.part,sub_part=subpart.get('part')).first()
                        if subpartinstance: 
                            subpart['req_store_qty']= subpart['req_qty']
                            subpart['req_qty']=subpartinstance.sub_part_qty
                        if StockMaster.objects.filter(part=subpart.get('part')).exists():
                            stock_avail=StockMaster.objects.get(part=subpart.get('part'))
                           
                            subpart['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
                        else:
                            subpart['stock_avail'] = 0

                        subpartstatus.append(subpart['status'])
                            # print(subpart,subpartinstance.sub_part_qty)
                all_subparts_complete=False
                if len(subpartstatus)<0:
                
                    all_subparts_complete = all(subpartstatus)
                assem_status.append(all_subparts_complete)
                # print(all_subparts_complete)
                assembly_list.append({
                    "mrs_id":assem.mrs_id,
                    "mrs_no":assem.mrs_no,
                    "ioa_no":assem.ioa_no,
                    "issue_by":assem.issue_by,
                    "part":assem.part.part_id,
                    "product_part_name":assem.part.product_part_name,
                    "product_part_no":assem.part.product_part_no,
                    "product_descp":assem.part.product_descp,
                    "req_qty":assem.req_qty,
                    "subpart":subparts
                })

        data['assembly_list']=assembly_list
        all_assem_complete=False
        if len(assem_status)>0:
            all_assem_complete=all(assem_status)

        part_list = MrsDetails.objects.filter(mrs=instance.mrs_id,type='P').values(
            'part',  
            'req_qty',
            'issue_qty',
            'mrs_detail_id',
            'ioa_no',
            'status',
            'type',
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_cost=F('part__product_cost'),
            # part_desc=F('part__product_descp'),
            product_descp=F('part__product_descp'),
            uom=F('part__uom'),
        )
        partstatus=[]
        for pl in part_list:
            if StockMaster.objects.filter(part=pl['part']).exists():
                stock_avail=StockMaster.objects.get(part=pl['part'])
               
                pl['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
            else:
                pl['stock_avail'] = 0
            partstatus.append(pl['status'])
        # print("all part status=>",partstatus)
        all_parts_complete=False
        
        if len(partstatus)<0:
            all_parts_complete = all(partstatus)

       
        # print('all_parts_complete=>',all_parts_complete)
        
        raw_mat_list = MrsDetails.objects.filter(mrs=instance.mrs_id,type='RM').values(
            'req_qty',
            'issue_qty',
            'mrs_detail_id',
            'ioa_no',
            'status',
            'rm',
            'type',
            rm_mat_name=F('rm__rm_mat_name'),
            rm_mat_code=F('rm__rm_mat_code'),
            rm_mat_desc=F('rm__rm_mat_desc')
        )
        rmstatus=[]
        for rm in raw_mat_list:  
            print(rm)     
            if StockMaster.objects.filter(rm=rm.get('rm')).exists():
                stock_avail=StockMaster.objects.filter(rm=rm.get('rm'))[0]
                print(stock_avail)
                print(stock_avail.stock_avail)
                rm['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
            else:
                rm['stock_avail'] = 0
            rmstatus.append(rm['status'])
        # print("all rm status=>",rmstatus)
        
        all_rm_complete=False
        
        if len(rmstatus)<0:
            all_rm_complete=all(rmstatus)

        # print('all_rm_complete=>',all_rm_complete)
        data['from_dept_name'] = instance.from_dept.dept_name if instance.from_dept else None

        data['part_list'] = part_list
        data['raw_mat_list'] = raw_mat_list
       
       
        data['status_complete']= (all_parts_complete and all_assem_complete and all_rm_complete)

        return data
    

    def update(self, instance: MrsMaster, validated_data):
        user_request = self.context['request'].user
        validated_data['modify_by'] = user_request.id
        partlist = validated_data.get('part_list')
     
        raw_mat_list = validated_data.get('raw_mat_list')
        assemby_list = validated_data.get('assembly_list',None)
   
        
   
        validated_data.pop('assembly_list', None)
      
        validated_data.pop('part_list', None)
        validated_data.pop('raw_mat_list', None)
        # print(assemby_list)
        try:
            l_min_id = MrsMaster.objects.latest('min_no')
        except MrsMaster.DoesNotExist:
            l_min_id=None
      
       
        # print(l_mrs_id.mrs_no)
        new_min_id =  1

        latest_min_no = l_min_id.min_no if l_min_id else None     
        if latest_min_no:  
            # Increment the latest mrs_id by 1
            current_min_id = int(latest_min_no[3:])
            new_min_id = current_min_id + 1
            print(new_min_id)
      
        formatted_min_no = 'MIN{:05d}'.format(new_min_id)
        if not instance.min_no:
            validated_data['min_no'] = formatted_min_no
        validated_data['status']=True
        validated_data['modify_date'] = timezone.now()
           
        # global global_avail_stock 
        if partlist is not None:
            try:
                decoded_part_list = json.loads(partlist)
                if len(decoded_part_list) >0:

                    print(decoded_part_list)
                    existing_records = MrsDetails.objects.filter(
                        Q(mrs=instance.mrs_id)
                    )
                    update_part_master_id_list = [part.get(
                        'mrs_detail_id') for part in decoded_part_list if part.get('mrs_detail_id')]
                    add_part_master_id_list = [
                        part for part in decoded_part_list if not part.get('mrs_detail_id')]
                    # existing_records_list = list(existing_records.values_list('mrs_detail_id', flat=True))
                    # delete_part_list = list(set(existing_records_list) - set(update_part_master_id_list))
                    
                    #backup code develop by OM
                    for part in decoded_part_list:
                        part.pop('stock_avail')
                        if part.get('mrs_detail_id') in update_part_master_id_list:
                            mrdinstance = MrsDetails.objects.get(
                                mrs_detail_id=part['mrs_detail_id'])
                            stoc_obj=StockMaster.objects.get(part=part['part'])
                            print( mrdinstance.issue_qty," check mrdinstance.issue_qty")
                            if int(part.get('issue_qty')) <=int(part.get('req_qty',mrdinstance.req_qty)):
                                if mrdinstance.issue_qty and mrdinstance.issue_qty!=0:
                                    print(stoc_obj.stock_avail,"first check stock")
                                    # stoc_aval=int(stoc_obj.stock_avail+mrdinstance.issue_qty)
                                    stoc_aval=stoc_obj.stock_avail
                                    print(stoc_obj.stock_avail, "part check stoc_obj.stock_avail available")
                                    print(mrdinstance.issue_qty, "part check mrdinstance.issue_qty available")
                                    print(stoc_aval, "part check stock available")
                                    # print("0000000  part 00000000")
                                    # print("part_no ==> ",mrdinstance.part.part_id ,"old issued =>",mrdinstance.issue_qty," new issued => ",part.get('issue_qty'))
                                    # print("part_no ==> ",mrdinstance.part.part_id ,"old stoc =>",stoc_obj.stock_avail," new stoc => ",stoc_aval)
                                    print("1 check stock===>",validated_data.get('is_close') and stoc_obj.stock_avail >0,stoc_obj.stock_avail >0,validated_data.get('is_close'),stoc_obj.stock_avail)

                                    if validated_data.get('is_close') and stoc_aval > 0:
                                        print("av last part===>",stoc_aval-int(part.get('issue_qty')),stoc_aval, part.get('issue_qty'), )
                                        StockMaster.objects.filter(part=part['part']).update(stock_avail=stoc_aval-int(part.get('issue_qty')))

                                        StockReserv.objects.filter(part=part['part']).update(issue_qty=part.get('issue_qty'),issue_date=timezone.now())
                                        serializer = StockUpdate_Serializers(data={
                                                    "part":part['part'],
                                                    "stock_avail": stoc_obj.stock_avail,
                                                    "stock_ui": stoc_obj.stock_ui,
                                                    "stock_reserv": stoc_obj.stock_reserv,
                                                    "stock_rej": stoc_obj.stock_rej,
                                                    "updt_date": timezone.now(),
                                                    "updt_by": user_request.id,
                                                    "tran_type": "Update",
                                                })
                                        if serializer.is_valid():
                                            serializer.save()
                                        else:
                                            print("stock Update add error => ", serializer.errors)
                                else:
                                    print("2 check stock====>",(validated_data.get('is_close') and stoc_obj.stock_avail >0),stoc_obj.stock_avail >0,validated_data.get('is_close'),stoc_obj.stock_avail)

                                    if validated_data.get('is_close') and stoc_obj.stock_avail >0:
                                        # print(part.get('issue_qty'),"else part")
                                        if stoc_obj.stock_avail-int(part.get('issue_qty',0))>=0:
                                        
                                            StockMaster.objects.filter(part=part['part']).update(stock_avail=stoc_obj.stock_avail-int(part.get('issue_qty')))

                                            StockReserv.objects.filter(part=part['part']).update(issue_qty=part.get('issue_qty'),issue_date=timezone.now())
                                            serializer = StockUpdate_Serializers(data={
                                                        "part":part['part'],
                                                        "stock_avail": stoc_obj.stock_avail,
                                                        "stock_ui": stoc_obj.stock_ui,
                                                        "stock_reserv": stoc_obj.stock_reserv,
                                                        "stock_rej": stoc_obj.stock_rej,
                                                        "updt_date": timezone.now(),
                                                        "updt_by": user_request.id,
                                                        "tran_type": "Update",
                                                    })
                                            if serializer.is_valid():
                                                serializer.save()
                                            else:
                                                print("stock Update add error => ", serializer.errors)
                                        else:
                                            print("issue qty is stockout")
                                            # raise serializers.ValidationError({"issue_qty":["issue qty is stockout"]})

                                part['mrs'] = instance.mrs_id
                                part['req_qty'] = int(part.get('req_qty',mrdinstance.req_qty))
                                part['type']='P'
                                if part.get('req_qty') and part.get('issue_qty'):
                                    if int(part.get('req_qty',mrdinstance.req_qty)) == int(part.get('issue_qty')):
                                        part['status']=True
                                    else:
                                        part['status']=False
                                    
                                serializer = MrsDetailSerializer(
                                    instance=mrdinstance, data=part)
                                # print("update  part list => ", part)

                             

                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    print(serializer.errors)

                            else:
                                print("<=====issue else ====>")

            except json.JSONDecodeError as e:
                print("partlist json: ", e)
        if assemby_list is not None:
            try:
                decoded_assemby_list = json.loads(assemby_list)
                if len(decoded_assemby_list) >0:

                   
                    existing_records = MrsMaster.objects.filter(
                        Q(mrs_id=instance.mrs_id)
                    )
                    update_assembly_master_id_list = [part.get(
                        'mrs_id') for part in decoded_assemby_list if part.get('mrs_id')]
                    add_part_master_id_list = [
                        part for part in decoded_assemby_list if not part.get('mrs_id')]
                    # existing_records_list = list(existing_records.values_list('mrs_detail_id', flat=True))
                    # delete_part_list = list(set(existing_records_list) - set(update_part_master_id_list))
                    print("update_assembly_master_id_list=>",update_assembly_master_id_list)
                    for assembly in decoded_assemby_list:
                        if assembly.get('mrs_id') in update_assembly_master_id_list:
                            mrinstance = MrsMaster.objects.get(mrs_id= assembly.get('mrs_id'),type=1)

                            subpartassem= assembly.get('subpart',[])
                            # print(mrinstance,subpartassem) 
                            if mrinstance:

                                #Backup code for subpar developed by OM
                                for subpart in subpartassem:
                                    subpart.pop('stock_avail')
                                    if subpart.get('mrs_detail_id'):
                                        mrdinstance = MrsDetails.objects.get(mrs_detail_id=subpart.get('mrs_detail_id'))
                                        stoc_obj=StockMaster.objects.get(part=mrdinstance.part)

                                        if mrdinstance.issue_qty and mrinstance.issue_qty!=0:
                                            stoc_aval=int(stoc_obj.stock_avail+mrdinstance.issue_qty)
                                            print(stoc_obj.stock_avail, "check stoc_obj.stock_avail available")
                                            print(mrdinstance.issue_qty, "check mrdinstance.issue_qty available")
                                            print(stoc_aval, "check stock available")
                                            # print( subpart.get('issue_qty'),"0000000000 subpart 000000000000000",stoc_aval)
                                            # print("subpart_no ==> ",mrdinstance.part.part_id ,"old issued =>",mrdinstance.issue_qty," new issued => ",subpart.get('issue_qty'))
                                            # print("subpart_no ==> ",mrdinstance.part.part_id ,"old stoc =>",stoc_obj.stock_avail," new stoc => ",stoc_aval)
                                           
                                            # print("av stock last ===>",stoc_aval-int(subpart.get('issue_qty')) )
                                            StockMaster.objects.filter(part=mrdinstance.part).update(stock_avail=stoc_aval-int(subpart.get('issue_qty')) )
                                           
                                            
                                            StockReserv.objects.filter(part=mrdinstance.part).update(issue_qty=subpart.get('issue_qty'),issue_date=timezone.now())
                                            serializer = StockUpdate_Serializers(data={
                                                        "part":mrdinstance.part.part_id         ,
                                                        "stock_avail": stoc_obj.stock_avail,
                                                        "stock_ui": stoc_obj.stock_ui,
                                                        "stock_reserv": stoc_obj.stock_reserv,
                                                        "stock_rej": stoc_obj.stock_rej,
                                                        "updt_date": timezone.now(),
                                                        "updt_by": user_request.id,
                                                        "tran_type": "Update",
                                                    })
                                            if serializer.is_valid():
                                                serializer.save()
                                            else:
                                                print("stock Update add error => ", serializer.errors)
                                        else:
                                            if stoc_obj.stock_avail !=0:
                                                print(subpart.get('issue_qty'),"else subpart")
                                                StockMaster.objects.filter(part=mrdinstance.part).update(stock_avail=stoc_obj.stock_avail-int(subpart.get('issue_qty'))) 
                                               
                                                StockReserv.objects.filter(part=mrdinstance.part).update(issue_qty=subpart.get('issue_qty'),issue_date=timezone.now())
                                                serializer = StockUpdate_Serializers(data={
                                                            "part":mrdinstance.part.part_id         ,
                                                            "stock_avail": stoc_obj.stock_avail,
                                                            "stock_ui": stoc_obj.stock_ui,
                                                            "stock_reserv": stoc_obj.stock_reserv,
                                                            "stock_rej": stoc_obj.stock_rej,
                                                            "updt_date": timezone.now(),
                                                            "updt_by": user_request.id,
                                                            "tran_type": "Update",
                                                        })
                                                if serializer.is_valid():
                                                    serializer.save()
                                                else:
                                                    print("stock Update add error => ", serializer.errors)
                                                
                                
                                        subpart['mrs']=mrinstance.mrs_id
                                        subpartinstance=SubpartMaster.objects.filter(part=mrinstance.part,sub_part=subpart.get('part')).first()
                                        req_qty= int(assembly.get('req_qty',mrinstance.req_qty))
                                    # print("subpartinstance=>",subpartinstance,mrinstance.part,mrdinstance.part,mrdinstance)
                                        if subpartinstance:
                                            subpart['req_qty']=int(subpartinstance.sub_part_qty*req_qty)
                                        # print("subpart=>",subpart)
                                            if subpart.get('req_qty') and subpart.get('issue_qty'):
                                                if int(subpart.get('req_qty',mrdinstance.req_qty)) == int(subpart.get('issue_qty')):
                                                    subpart['status']=True
                                                else:
                                                    subpart['status']=False



                                        if int(subpart.get('issue_qty')) <=int(subpart.get('req_qty',mrdinstance.req_qty)):
                                        
                                            serializer = MrsDetailSerializer(data=subpart,instance=mrdinstance)
                                            if serializer.is_valid():
                                                serializer.save()
                                            else:
                                                print(serializer.errors)
                                    else:
                                        raise serializers.ValidationError({"assembly_subpart":["Subpart req_qty is required."]})
                            
  
                            assembly['mrs_date']=validated_data.get('mrs_date',mrinstance.mrs_date)
                            assembly['min_no']=formatted_min_no
                            assembly['from_dept']=validated_data.get('from_dept',mrinstance.mrs_date)
                            assembly['issue_by']=validated_data.get('issue_by',mrinstance.issue_by)
                            assembly['req_qty']=assembly.get('req_qty',mrinstance.req_qty)
                            assembly['prep_by']=validated_data.get('prep_by',mrinstance.prep_by)
                            assembly['remark']=validated_data.get('remark',mrinstance.remark)
                            assembly['auth_by']=validated_data.get('auth_by',mrinstance.auth_by)
                            assembly['ioa_no']=validated_data.get('ioa_no',mrinstance.ioa_no)
                            assembly.pop('subpart',None)
                            print("assembly =>",assembly)
                            part_instan= PartsMaster.objects.get(part_id=assembly.get('part'))
                            assembly['part']=part_instan
                            super().update(mrinstance, assembly)

                            print("update  assembly list")


            except json.JSONDecodeError as e:
                print("assemby json: ", e)
           
        if raw_mat_list is not None:
            try:
                decoded_raw_mat_list = json.loads(raw_mat_list)
                if len(decoded_raw_mat_list) >0:

                    print(decoded_raw_mat_list)
                    existing_records = MrsDetails.objects.filter(
                        Q(mrs=instance.mrs_id)
                    )
                    update_raw_mat_list_list = [rm.get(
                        'mrs_detail_id') for rm in decoded_raw_mat_list if rm.get('mrs_detail_id')]
                    add_raw_mat_list_list = [
                        rm for rm in decoded_raw_mat_list if not rm.get('mrs_detail_id')]
                    # existing_records_list = list(existing_records.values_list('mrs_detail_id', flat=True))
                    # delete_part_list = list(set(existing_records_list) - set(update_part_master_id_list))
                    for rm in decoded_raw_mat_list:
                        rm.pop('stock_avail',None)

                        if rm.get('mrs_detail_id') in update_raw_mat_list_list:
                            mrdinstance = MrsDetails.objects.get(
                                mrs_detail_id=rm['mrs_detail_id'])
                            stoc_obj=StockMaster.objects.get(rm=rm['rm'])
                            print( mrdinstance.issue_qty," check mrdinstance.issue_qty")
                            if mrdinstance.issue_qty and mrdinstance.issue_qty!=0:
                                stoc_aval=int(stoc_obj.stock_avail+mrdinstance.issue_qty)
                                if stoc_obj.stock_avail >0:
                                    if stoc_aval-int(rm.get('issue_qty',0))>=0:
                                        StockMaster.objects.filter(rm=rm['rm']).update(stock_avail=stoc_aval-int(rm.get('issue_qty')))
                                        StockReserv.objects.filter(rm=rm['rm']).update(issue_qty=rm.get('issue_qty'),issue_date=timezone.now())
                                        serializer = StockUpdate_Serializers(data={
                                                    "rm":rm['rm'],
                                                    "stock_avail": stoc_obj.stock_avail,
                                                    "stock_ui": stoc_obj.stock_ui,
                                                    "stock_reserv": stoc_obj.stock_reserv,
                                                    "stock_rej": stoc_obj.stock_rej,
                                                    "updt_date": timezone.now(),
                                                    "updt_by": user_request.id,
                                                    "tran_type": "Update",
                                                })
                                        if serializer.is_valid():
                                            serializer.save()
                                        else:
                                            print("stock Update add error => ", serializer.errors)
                                
                                
                                # print(stoc_obj.stock_avail, "RM check stoc_obj.stock_avail available")
                                # print(mrdinstance.issue_qty, "RM check mrdinstance.issue_qty available")
                                # print(stoc_aval, "RM check stock available")
                            
                            else:
                                 if stoc_obj.stock_avail >0:
                                    if stoc_obj.stock_avail-int(rm.get('issue_qty',0))>=0:
                                        print(stoc_obj.stock_avail-int(rm.get('issue_qty',0)), "RM check stock available")
                                        
                                        StockMaster.objects.filter(rm=rm['rm']).update(stock_avail=stoc_obj.stock_avail-int(rm.get('issue_qty')))
                                        StockReserv.objects.filter(rm=rm['rm']).update(issue_qty=rm.get('issue_qty'),issue_date=timezone.now())
                                        serializer = StockUpdate_Serializers(data={
                                                    "rm":rm['rm'],
                                                    "stock_avail": stoc_obj.stock_avail,
                                                    "stock_ui": stoc_obj.stock_ui,
                                                    "stock_reserv": stoc_obj.stock_reserv,
                                                    "stock_rej": stoc_obj.stock_rej,
                                                    "updt_date": timezone.now(),
                                                    "updt_by": user_request.id,
                                                    "tran_type": "Update",
                                                })
                                        if serializer.is_valid():
                                            serializer.save()
                                        else:
                                            print("stock Update add error => ", serializer.errors)
                            rm['req_qty'] = int(rm.get('req_qty',mrdinstance.req_qty))
                            rm['type']='RM'
                            rm['mrs'] = instance.mrs_id
                            if rm.get('req_qty') and rm.get('issue_qty'):
                                if int(rm.get('req_qty',mrdinstance.req_qty)) == int(rm.get('issue_qty')):
                                    rm['status']=True
                                else:
                                    rm['status']=False

                            serializer = MrsDetailSerializer(instance=mrdinstance, data=rm)
                            print("update  raw_mat list")
                        

                            if serializer.is_valid():
                                serializer.save()
                            else:
                                print(serializer.errors)
                      
                        
            except json.JSONDecodeError as e:
                print("rm json: ", e)
         
      

        return super().update(instance, validated_data)





class CIS_Serializers(serializers.ModelSerializer):
    part_list = serializers.CharField(
        required=False, write_only=True, default="[]")

    raw_mat_list = serializers.CharField(
        required=False, write_only=True, default="[]")
  
    assembly_list = serializers.CharField(required=False, write_only=True, default="[]")
   
    class Meta:
        model = MrsMaster
        exclude = []
        extra_kwargs = {
            "mrs_no": {
                'required': False
            },
            "status": {
                'required': False,
                'default': False
            },
              "modify_date":{
                "default":timezone.now()
            }
        }

    def to_representation(self, instance: MrsMaster):
        data = super().to_representation(instance)
        assembly_list=[]
        if MrsMaster.objects.filter(mrs_no=instance.mrs_no,type=True).exists():
            filterdata=MrsMaster.objects.filter(mrs_no=instance.mrs_no,type=True)
            print(filterdata,instance.mrs_id)
            for assem in filterdata:

                subparts= MrsDetails.objects.filter(mrs=assem,type="SP").values(
                        'part',  
                        'req_qty',
                        'issue_qty',
                        'mrs_detail_id',
                        'ioa_no',
                        'mrs',
                        'type',
                        product_part_no=F('part__product_part_no'),
                        product_part_name=F('part__product_part_name'),
                        product_cost=F('part__product_cost'),
                        # part_desc=F('part__product_descp'),
                        product_descp=F('part__product_descp'),
                        uom=F('part__uom'),
                )
                for subpart in subparts:
                    if subpart.get('type')=='SP':
                        subpartinstance=SubpartMaster.objects.filter(part=assem.part,sub_part=subpart.get('part')).first()
                        if subpartinstance: 
                            subpart['req_store_qty']= subpart['req_qty']
                            subpart['req_qty']=subpartinstance.sub_part_qty
                        if StockMaster.objects.filter(part=subpart.get('part')).exists():
                            stock_avail=StockMaster.objects.get(part=subpart.get('part'))
                           
                            subpart['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
                        else:
                            subpart[''] = 0  
                            # print(subpart,subpartinstance.sub_part_qty)
                
                assembly_list.append({  
                    "mrs_id":assem.mrs_id,
                    "mrs_no":assem.mrs_no,
                    "ioa_no":assem.ioa_no,
                    "issue_by":assem.issue_by,
                    "part":assem.part.part_id,
                    "product_part_name":assem.part.product_part_name,
                    "product_part_no":assem.part.product_part_no,
                    "product_descp":assem.part.product_descp,
                    "req_qty":assem.req_qty,
                    "subpart":subparts
                })

        data['assembly_list']=assembly_list
       

        part_list = MrsDetails.objects.filter(mrs=instance.mrs_id,type='P').values(
            'part',  
            'req_qty',
            'issue_qty',
            'mrs_detail_id',
            'ioa_no',
            'type',
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_cost=F('part__product_cost'),
            # part_desc=F('part__product_descp'),
            product_descp=F('part__product_descp'),
            uom=F('part__uom'),
        )
        for pl in part_list:
            if StockMaster.objects.filter(part=pl['part']).exists():
                stock_avail=StockMaster.objects.get(part=pl['part'])
                print(pl['part'],stock_avail.stock_avail)
                pl['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
            else:
                pl['stock_avail'] = 0
        raw_mat_list = MrsDetails.objects.filter(mrs=instance.mrs_id,type='RM').values(
            'req_qty',
            'issue_qty',
            'mrs_detail_id',
            'ioa_no',
            'rm',
            'type',
            rm_mat_name=F('rm__rm_mat_name'),
            rm_mat_code=F('rm__rm_mat_code'),
            rm_mat_desc=F('rm__rm_mat_desc'),

        )
        for rm in raw_mat_list:
            if StockMaster.objects.filter(rm=rm.get('rm')).exists():
                stock_avail=StockMaster.objects.filter(rm=rm.get('rm'))[0]
             
                rm['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
            else:
                rm['stock_avail'] = 0
        data['from_dept_name'] = instance.from_dept.dept_name if instance.from_dept else None

        data['part_list'] = part_list
        data['raw_mat_list'] = raw_mat_list

        return data
   
   
    def create(self, validated_data):
        user_request = self.context['request'].user
        validated_data['created_date'] = timezone.now()
        validated_data['create_by'] = user_request.id
        partlist = validated_data.get('part_list',None)
        assemby_list = validated_data.get('assembly_list',None)
     
        raw_mat_list = validated_data.get('raw_mat_list')
        print("data=> ",validated_data)    
        
        validated_data.pop('part_list', None)
        validated_data.pop('assembly_list', None)
    
        validated_data.pop('raw_mat_list', None)
    
      
        validated_data['status'] = True
        # Increment the latest mrs_id by 1
        try:
            l_min_id = MrsMaster.objects.latest('min_no')
        except MrsMaster.DoesNotExist:
            l_min_id=None
        try:
            l_mrs_id = MrsMaster.objects.latest('mrs_no') 

        except MrsMaster.DoesNotExist:
            l_mrs_id=None
       
       
        # print(l_mrs_id.mrs_no)
        new_min_id =  1
        new_mrs_id =  1

        latest_min_no = l_min_id.min_no if l_min_id else None     
        latest_mrs_no = l_mrs_id.mrs_no if l_mrs_id else None     
        if latest_min_no:  
            # Increment the latest mrs_id by 1
            current_min_id = int(latest_min_no[3:])
            new_min_id = current_min_id + 1
            print(new_min_id)
        if latest_mrs_no:  
            # Increment the latest mrs_id by 1
            current_mrs_id = int(latest_mrs_no[3:])
            new_mrs_id = current_mrs_id + 1
            print(new_mrs_id)
      
        formatted_mrs_id = 'MRS{:04d}'.format(new_mrs_id)
        formatted_min_id = 'CIS{:04d}'.format(new_min_id)
        validated_data['mrs_no'] = formatted_mrs_id
        validated_data['min_no'] = formatted_min_id
        validated_data['type'] = 0
        print("data=> ",validated_data)    
        
        mrs = super().create(validated_data)
        mrsObj = MrsMaster.objects.get(mrs_id=mrs.mrs_id)
        
        if partlist is not None:
                try:
                    decoded_part_list = json.loads(partlist)
                    if len(decoded_part_list) >0:
                            decoded_part_list = json.loads(partlist)
                           
                            for part in decoded_part_list:
                                stoc_obj=StockMaster.objects.get(part=part['part'])

                                part['mrs'] = mrsObj.mrs_id
                                part['type']='P'
                                # print("part=>", part)
                                serializer = MrsDetailSerializer(data=part)
                                if serializer.is_valid():
                                    serializer.save()
                                    if stoc_obj.stock_avail >0:
                                        if stoc_obj.stock_avail-int(part.get('issue_qty',0))>0:
                                            StockMaster.objects.filter(part=part['part']).update(stock_avail=stoc_obj.stock_avail-int(part.get('issue_qty')))
                                            StockReserv.objects.filter(part=part['part']).update(issue_qty=part.get('issue_qty'),issue_date=timezone.now())
                                            serializer = StockUpdate_Serializers(data={
                                                        "part":part['part'],
                                                        "stock_avail": stoc_obj.stock_avail,
                                                        "stock_ui": stoc_obj.stock_ui,
                                                        "stock_reserv": stoc_obj.stock_reserv,
                                                        "stock_rej": stoc_obj.stock_rej,
                                                        "updt_date": timezone.now(),
                                                        "updt_by": user_request.id,
                                                        "tran_type": "Update",
                                                    })
                                            if serializer.is_valid():
                                                serializer.save()
                                            else:
                                                print("stock Update add error => ", serializer.errors)
                                else:
                                    print(serializer.errors)
                except json.JSONDecodeError as e:
                    print("partlist json: ", e)
        if assemby_list is not None:
            try:
                decoded_assemby_list = json.loads(assemby_list)
              
                if len(decoded_assemby_list) > 0: 
                        for assembly in decoded_assemby_list:
                                print(assembly)
                                part_inst= PartsMaster.objects.get(part_id=assembly.get('part'))
                                mrs_assembly = MrsMaster.objects.create(mrs_no=formatted_mrs_id,min_no=formatted_min_id,issue_qty=assembly.get('issue_qty'),
                                                               mrs_date=validated_data.get('mrs_date'),part=part_inst,req_qty=assembly.get('req_qty'),
                                                               from_dept=validated_data.get('from_dept'),prep_by=validated_data.get('prep_by'),auth_by=validated_data.get('auth_by')
                                                               ,issue_by=validated_data.get('issue_by'),ioa_no=assembly.get('ioa_no'),remark=validated_data.get('remark'),
                                                               create_by=user_request.id,created_date=timezone.now(),modify_by=user_request.id,modify_date=timezone.now(),type=1,status=1
                                                               )
                                
                                subpartassem= assembly.get('subpart',[])
                                for subpart in subpartassem:
                                    subpart['mrs'] = mrs_assembly.mrs_id
                                    req_qty= int(assembly.get('req_qty',1))
                                    subpart['part']=subpart['sub_part_id']
                                    subpart['type']='SP'
                                    subpart['req_qty']=subpart['sub_part_qty']*req_qty
                                    serializer = MrsDetailSerializer(data=subpart)
                                    if serializer.is_valid():
                                        serializer.save()
                                        stoc_obj=StockMaster.objects.get(part=subpart['part'])
                                        if stoc_obj.stock_avail >0:
                                            if stoc_obj.stock_avail-int(subpart.get('issue_qty',0))>0:
                                                StockMaster.objects.filter(part=subpart['part']).update(stock_avail=stoc_obj.stock_avail-int(subpart.get('issue_qty')))
                                                StockReserv.objects.filter(part=subpart['part']).update(issue_qty=subpart.get('issue_qty'),issue_date=timezone.now())
                                                serializer = StockUpdate_Serializers(data={
                                                            "part":subpart['part'],
                                                            "stock_avail": stoc_obj.stock_avail,
                                                            "stock_ui": stoc_obj.stock_ui,
                                                            "stock_reserv": stoc_obj.stock_reserv,
                                                            "stock_rej": stoc_obj.stock_rej,
                                                            "updt_date": timezone.now(),
                                                            "updt_by": user_request.id,
                                                            "tran_type": "Update",
                                                        })
                                                if serializer.is_valid():
                                                    serializer.save()
                                                else:
                                                    print("stock Update add error => ", serializer.errors)
                                    else:
                                        print(serializer.errors)
                                    
                          
            except json.JSONDecodeError as e:
                    print("assemby json: ", e)

        
        if raw_mat_list is not None:
                try:
                    decoded_raw_mat_list = json.loads(raw_mat_list)
                    if len(decoded_raw_mat_list) >0:
                       
                        print("RAW MAT",len(raw_mat_list))
                        print(decoded_raw_mat_list)
                        for rm in decoded_raw_mat_list:
                            rm['mrs'] = mrsObj.mrs_id
                            rm['type']='RM'

                            serializer = MrsDetailSerializer(data=rm)
                            if serializer.is_valid():
                                serializer.save()
                                stoc_obj=StockMaster.objects.get(rm=rm['rm'])
                                if stoc_obj.stock_avail >0:
                                    if stoc_obj.stock_avail-int(rm.get('issue_qty',0))>0:
                                        StockMaster.objects.filter(rm=rm['rm']).update(stock_avail=stoc_obj.stock_avail-int(rm.get('issue_qty')))
                                        StockReserv.objects.filter(rm=rm['rm']).update(issue_qty=rm.get('issue_qty'),issue_date=timezone.now())
                                        serializer = StockUpdate_Serializers(data={
                                                    "rm":rm['rm'],
                                                    "stock_avail": stoc_obj.stock_avail,
                                                    "stock_ui": stoc_obj.stock_ui,
                                                    "stock_reserv": stoc_obj.stock_reserv,
                                                    "stock_rej": stoc_obj.stock_rej,
                                                    "updt_date": timezone.now(),
                                                    "updt_by": user_request.id,
                                                    "tran_type": "Update",
                                                })
                                        if serializer.is_valid():
                                            serializer.save()
                                        else:
                                            print("stock Update add error => ", serializer.errors)
                            else:
                                print(serializer.errors)

                except json.JSONDecodeError as e:
                    print("raw_mat_list json: ", e)
        
        
        return super().update(mrsObj, validated_data)

 


# class Raw_MaterialSerializers(serializers.ModelSerializer):
    class Meta:
        model = RawMaterialMaster
        exclude = []

    def to_representation(self, instance):
        data=super().to_representation(instance)
        if StockMaster.objects.filter(rm=instance).exists():
                stock_avail=StockMaster.objects.filter(rm=instance)
                print(stock_avail[0].stock_avail)
                data['stock_avail'] = int(stock_avail[0].stock_avail) if stock_avail[0].stock_avail is not None else 0
        else:
                data['stock_avail'] = 0
        return data
    def create(self, validated_data):
        print(validated_data)
        requestuser = self.context['request'].user
        validated_data['create_by'] = requestuser.id
        validated_data['created_date'] = timezone.now()
        validated_data['rm_mat_desc'] = str(validated_data.get(
            'rm_mat_name')+' '+validated_data.get('rm_sec_type', ' ')+' '+validated_data.get('rm_size', ' '))
        max_rm_mat_code = RawMaterialMaster.objects.all().aggregate(Max('rm_id'))[
            'rm_id__max']

# Increment by 1 if not None, else set to 1
        rm_mat_code_id = int(max_rm_mat_code) +  1 if max_rm_mat_code is not None else 1
        validated_data['rm_mat_code'] = rm_mat_code_id
        rm_mat_id=super().create(validated_data)
        StockMaster.objects.create(rm=rm_mat_id,type=2,stock_avail=0,stock_ui=0,stock_reserv=0,stock_rej=0,last_update=timezone.now())

        return rm_mat_id

    def update(self, instance, validated_data):
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        print(validated_data)
        # if validated_data.get('rm_mat_name'):
        #     validated_data['rm_mat_desc'] = str(validated_data.get('rm_mat_name', instance.rm_mat_name) if validated_data.get('rm_mat_name', instance.rm_mat_name) else ''+' '+validated_data.get(
        #     'rm_sec_type', instance.rm_sec_type) if validated_data.get('rm_sec_type', instance.rm_sec_type) else '' +' '+validated_data.get('rm_size', instance.rm_size) if validated_data.get('rm_size', instance.rm_size) else '')

        return super().update(instance, validated_data)


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentMaster
        exclude = []
        extra_kwargs = {

            "create_date": {
                "required": False
            },
            "create_by": {
                "required": False
            },

        }

    def validate_dept_name(self, value):
        # Get the current assemblies instance being updated
        dept: DepartmentMaster = self.instance
        if dept is not None and dept.dept_name == value:
            return value  # a_no not changed, no need to perform validation

        if DepartmentMaster.objects.filter(dept_name=value).exists():
            raise serializers.ValidationError(
                "The department name is already taken.")
        return value

    def create(self, validated_data):
        requestuser = self.context['request'].user
        validated_data['create_by'] = requestuser.id
        validated_data['create_date'] = timezone.now()

        return super().create(validated_data)

    def update(self, instance, validated_data):
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()

        return super().update(instance, validated_data)

class PurchRequistionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchRequistionDetails
        exclude = []


class  PurchRequistReturnSerializer(serializers.ModelSerializer):
    part_list = serializers.CharField(required=True, write_only=True)
    del_part_list=serializers.CharField(required=False, write_only=True)
   
    class Meta:
        model = PurchRequistion
        exclude = []
        extra_kwargs = {
            "pr_no": {
                "required": False
            },
            
            "pr_lvl_1_approved": {
                "required": False
            },
            "pr_lvl_2_approved": {
                "required": False
            },

        }
    
    def update_notifications_to_read(self, status, user_id, pr_id):
        notification=Notification.objects.filter(
            type=status, receiver_user=user_id, action=pr_id
        )
        for notifi in notification:
            notifi.is_read=True
            notifi.save()
    @transaction.atomic
    def update(self, instance:PurchRequistion, validated_data):
        part_list = validated_data.pop('part_list', None)
        del_part_list = validated_data.pop('del_part_list', None)
        serializer_list=[]
        serializer_createlist=[]
        serializer_errorcreatelist=[]
        requestuser = self.context['request'].user
        validated_data['pr_status']="PR_UNDER_APPROVAL"
        serializer_error_list=[]
        if del_part_list is not None or del_part_list != "":
            try:
                convertdelpart_listJson = json.loads(del_part_list) 
                PurchRequistionDetails.objects.filter(prd_id__in=convertdelpart_listJson).delete()
            except Exception as e:
                print(e)
                
        if part_list is not None or part_list != "":
            try:
                convertpart_listJson = json.loads(part_list) 
                for item in convertpart_listJson:
                    if item.get('prd_id'):

                        item['pr'] = instance.pr_id
                        instanceprd = PurchRequistionDetails.objects.get(prd_id=item.get('prd_id')) 
                        serializer = PurchRequistionDetailsSerializer(data=item,instance=instanceprd)
                        if serializer.is_valid():
                                serializer_list.append(serializer)
                        else:                    
                            serializer_error_list.append(serializer.errors)
                    else:
                        item['pr'] = instance.pr_id

                        serializer = PurchRequistionDetailsSerializer(data=item)
                        if serializer.is_valid():
                                serializer_createlist.append(serializer)
                        else:                    
                            serializer_errorcreatelist.append(serializer.errors)
            
            except Exception as e:
                print(e)
                raise serializers.ValidationError({"part_list":f"partlist json error : {e}"})

        if len(serializer_errorcreatelist)!=0:
            print("serializer_error_list=====",serializer_errorcreatelist) 
           
            raise serializers.ValidationError({"part_list":serializer_error_list})
        else:
            for user_serial in serializer_createlist:
                        user_serial.save()  

        if len(serializer_error_list)!=0 :
            print("serializer_error_list=====",serializer_error_list) 
            raise serializers.ValidationError({"part_list":serializer_error_list})
        else:
            for user_serial in serializer_list:
                        user_serial.save()    
 
          
            self.update_notifications_to_read('PR_Return',requestuser.id,instance.pr_id)
            if instance.pr_approval_level == 1:
                notification_message = f"A purchase requisition with the code {instance.pr_no} has been generated. Please click here to approve the PR."  

                notification_user = AuthUser.objects.get(pk=instance.pr_approval_lvl_1_users)
                notification = Notification.objects.create(
                    type='PR_Approval',
                    message=notification_message,
                    created_date=timezone.now(),
                    sender_user_id=instance.pr_create_by,
                    receiver_user=notification_user,
                    action=instance.pr_id,
                    is_read=False
                )
            if instance.pr_approval_level == 2:
                notification_message = f"A purchase requisition with the code {instance.pr_no} has been generated. Please click here to approve the PR."  

                notification_user = AuthUser.objects.get(pk=instance.pr_approval_lvl_1_users)
                notification = Notification.objects.create(
                    type='PR_Approval',
                    message=notification_message,
                    created_date=timezone.now(),
                    receiver_user=notification_user,
                    sender_user_id=instance.pr_create_by,
                    action=instance.pr_id,
                    is_read=False
                )
            self.update_notifications_to_read("PR_Return",requestuser.id, instance.pr_id)
            instance.pr_lvl_1_approved=False
            instance.pr_lvl_2_approved=False
        return super().update(instance, validated_data)

class PurchRequistSerializer(serializers.ModelSerializer):
    part_list = serializers.CharField(required=True, write_only=True,allow_null=True,)
    del_part_list=serializers.CharField(required=False, write_only=True)
    rm_list = serializers.CharField(required=True, write_only=True,allow_null=True)
    del_rm_list=serializers.CharField(required=False, write_only=True)
    class Meta:
        model = PurchRequistion
        exclude = []
        extra_kwargs = {
            "pr_no": {
                "required": False
            },
            
            "pr_lvl_1_approved": {
                "required": False
            },
            "pr_lvl_2_approved": {
                "required": False
            },

        }

    def to_representation(self, instance: PurchRequistion):
        data = super().to_representation(instance)        
        if instance.dept:
            data['dept_name'] = instance.dept.dept_name
        if instance.type=="PART":
        
            part_list = PurchRequistionDetails.objects.filter(pr=instance.pr_id).values(
            'part',  
            'pr',
            'prd_id',
            'part_qty',
            'ioa_no',       
            'type',     
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_cost=F('part__product_cost'),
            product_descp=F('part__product_descp'),
            uom=F('part__uom'),
        )
            for part in part_list:
                stock=StockMaster.objects.filter(part=part.get('part'))
                part['stock_avail']=stock[0].stock_avail if stock else 0
            
        
            data["part_list"] = part_list
        pr_approval_lvl_1_users_list=AuthUser.objects.filter(id=data.get('pr_approval_lvl_1_users')).values()
        pr_approval_lvl_2_users_list=AuthUser.objects.filter(id=data.get('pr_approval_lvl_2_users')).values()
        data['user_level1']=pr_approval_lvl_1_users_list
        data['user_level2']=pr_approval_lvl_2_users_list


        if instance.type=="RM":

            rm_list = PurchRequistionDetails.objects.filter(pr=instance.pr_id).values(
            'rm',        
            'part_qty',
            'ioa_no',    
            rm_mat_name=F('rm__rm_mat_name'),                  
            rm_mat_code=F('rm__rm_mat_code'),                  
            rm_mat_desc=F('rm__rm_mat_desc'),                   
            rm_sec_type=F('rm__rm_sec_type'),                   
            rm_size=F('rm__rm_size'),                   
            hsn_code=F('rm__hsn_code'),                   
            rm_cost=F('rm__rm_cost'),                   
            uom=F('rm__uom'),                     
            rm_image=F('rm__rm_image'),                   
            drawing_no=F('rm__drawing_no'),                   
            )
            for rm in rm_list:
                stock=StockMaster.objects.filter(rm=rm.get('rm'))
                rm['stock_avail']=stock[0].stock_avail if stock else 0
            
            data['rm_list'] = rm_list
                
        return data

    def generate_pr_no(self):
        # Extract PO number generation into its own method
        initial_offset = 1
        total_po_count = PurchRequistion.objects.count()
        new_po_id = total_po_count + initial_offset
        return 'PR{:04d}'.format(new_po_id)
    def handleCreatePartList(self,part_list,instance):
        serializer_list=[]
        serializer_error_list=[]
        if part_list is not None or part_list != "" or part_list != "[]":
            try:
                convertpart_listJson = json.loads(part_list) 

                for item in convertpart_listJson:
                    print(item)
                    item['pr'] = instance.pr_id
                    item['type'] = "PART"
                    serializer = PurchRequistionDetailsSerializer(data=item)
                    if serializer.is_valid():
                            serializer_list.append(serializer)
                    else:                    
                        serializer_error_list.append(serializer.errors)
            except Exception as e:
                print(e)
                raise serializers.ValidationError({"part_list":f"partlist json error : {e}"})
        if len(serializer_error_list)!=0:
            print("serializer_error_list=====",serializer_error_list) 
            PurchRequistion.objects.filter(pr_id=instance.pr_id).delete()
            raise serializers.ValidationError({"part_list":serializer_error_list})
        else:
            for user_serial in serializer_list:
                        user_serial.save()
    def handleCreateMaterialList(self,rm_list,instance):
        serializer_list=[]
        serializer_error_list=[]
        if rm_list is not None or rm_list != "" or rm_list != "[]":
            try:
                convertrm_listJson = json.loads(rm_list) 

                for item in convertrm_listJson:
                    print(item)
                    item['pr'] = instance.pr_id
                    item['type'] = "RM"

                    serializer = PurchRequistionDetailsSerializer(data=item)
                    if serializer.is_valid():
                            serializer_list.append(serializer)
                    else:                    
                        serializer_error_list.append(serializer.errors)
            except Exception as e:
                print(e)
                raise serializers.ValidationError({"rm_list":f"rm list json error : {e}"})
        if len(serializer_error_list)!=0:
            print("serializer_error_list=====",serializer_error_list) 
            PurchRequistion.objects.filter(pr_id=instance.pr_id).delete()
            raise serializers.ValidationError({"rm_list":serializer_error_list})
        else:
            for user_serial in serializer_list:
                        user_serial.save()
    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        part_list = validated_data.pop('part_list', None)
        rm_list = validated_data.pop('rm_list', None)
        validated_data.pop('del_part_list', None)
        validated_data.pop('del_rm_list', None)
        validated_data['pr_status']='PR_UNDER_APPROVAL'
        requestuser = self.context['request'].user
        validated_data['pr_create_by'] = requestuser.id
        validated_data['pr_date'] = timezone.now().date()
        validated_data['pr_no']=self.generate_pr_no()
        
        pr = super().create(validated_data)

        if validated_data.get('type')=="PART":
            self.handleCreatePartList(part_list,pr)
        elif validated_data.get('type')=="RM":
            self.handleCreateMaterialList(rm_list,pr)
        return pr
    
    def handleUpdatePartList(self,part_list,instance):
        serializer_list=[]
        serializer_error_list=[]
        serializer_createlist=[]
        serializer_errorcreatelist=[]
        if part_list is not None or part_list != "" or part_list!='[]':
            try:
                convertpart_listJson = json.loads(part_list) 
                for item in convertpart_listJson:
                    if item.get('prd_id'):

                        item['pr'] = instance.pr_id
                        item['type']='PART'
                        instanceprd = PurchRequistionDetails.objects.get(prd_id=item.get('prd_id')) 
                        serializer = PurchRequistionDetailsSerializer(data=item,instance=instanceprd)
                        if serializer.is_valid():
                                serializer_list.append(serializer)
                        else:                    
                            serializer_error_list.append(serializer.errors)
                    else:
                        item['pr'] = instance.pr_id

                        serializer = PurchRequistionDetailsSerializer(data=item)
                        if serializer.is_valid():
                                serializer_createlist.append(serializer)
                        else:                    
                            serializer_errorcreatelist.append(serializer.errors)
            
            except Exception as e:
                print(e)
                raise serializers.ValidationError({"part_list":f"partlist json error : {e}"})

        if len(serializer_errorcreatelist)!=0:
            print("serializer_error_list=====",serializer_errorcreatelist) 
           
            raise serializers.ValidationError({"part_list":serializer_error_list})
        else:
            for user_serial in serializer_createlist:
                        user_serial.save()  

        if len(serializer_error_list)!=0 :
            print("serializer_error_list=====",serializer_error_list) 
            raise serializers.ValidationError({"part_list":serializer_error_list})
        else:
            for user_serial in serializer_list:
                        user_serial.save()    
    def handleUpdateRrList(self,rm_list,instance):
        serializer_list=[]
        serializer_error_list=[]
        serializer_createlist=[]
        serializer_errorcreatelist=[]
        if rm_list is not None or rm_list != "" or rm_list != "[]":
            try:
                convertrm_listJson = json.loads(rm_list) 
                for item in convertrm_listJson:
                    if item.get('prd_id'):

                        item['pr'] = instance.pr_id
                        item['type']='RM'

                        instanceprd = PurchRequistionDetails.objects.get(prd_id=item.get('prd_id')) 
                        serializer = PurchRequistionDetailsSerializer(data=item,instance=instanceprd)
                        if serializer.is_valid():
                                serializer_list.append(serializer)
                        else:                    
                            serializer_error_list.append(serializer.errors)
                    else:
                        item['pr'] = instance.pr_id

                        serializer = PurchRequistionDetailsSerializer(data=item)
                        if serializer.is_valid():
                                serializer_createlist.append(serializer)
                        else:                    
                            serializer_errorcreatelist.append(serializer.errors)
            
            except Exception as e:
                print(e)
                raise serializers.ValidationError({"rm_list":f"rm_list json error : {e}"})

        if len(serializer_errorcreatelist)!=0:
            print("serializer_error_list=====",serializer_errorcreatelist) 
           
            raise serializers.ValidationError({"rm_list":serializer_error_list})
        else:
            for user_serial in serializer_createlist:
                        user_serial.save()  

        if len(serializer_error_list)!=0 :
            print("serializer_error_list=====",serializer_error_list) 
            raise serializers.ValidationError({"rm_list":serializer_error_list})
        else:
            for user_serial in serializer_list:
                        user_serial.save()    
    @transaction.atomic
    def update(self, instance, validated_data):
        part_list = validated_data.pop('part_list', None)
        rm_list = validated_data.pop('rm_list', None)
        del_part_list = validated_data.pop('del_part_list', None)
        del_rm_list = validated_data.pop('del_rm_list', None)
      
        if del_part_list is not None or del_part_list != "":
            try:
                convertdelpart_listJson = json.loads(del_part_list) 
                PurchRequistionDetails.objects.filter(prd_id__in=convertdelpart_listJson).delete()
            except Exception as e:
                print(e)
        if del_rm_list is not None or del_rm_list != "":
            try:
                convertdelrm_listJson = json.loads(del_rm_list) 
                PurchRequistionDetails.objects.filter(prd_id__in=convertdelrm_listJson).delete()
            except Exception as e:
                print(e)
        if instance.type=="PART":
            self.handleUpdatePartList(part_list,instance)
        elif instance.type=="RM":
            self.handleUpdateRrList(rm_list,instance)
        return super().update(instance, validated_data)


class Rm_Store_Location(serializers.ModelSerializer):
    class Meta:
        model = RmStoreLocation
        exclude = []

class Raw_MaterialSerializers(serializers.ModelSerializer):
    rm_row_no = serializers.CharField(required=False, write_only=True)
    rm_rack_no = serializers.CharField(required=True, write_only=True)
    rm_shelf_no = serializers.CharField(required=False, write_only=True)
    rm_tub_no = serializers.CharField(required=True, write_only=True)
    remark = serializers.CharField(required=False, write_only=True)

    rm_image_uploads = serializers.FileField(write_only=True,required=False)

    del_rm_image =serializers.BooleanField(default=False, required=False, write_only=True)

    class Meta:
        model = RawMaterialMaster
        exclude = []
        extra_kwargs = {
            "rm_image":{
                "required": False
            },
        }

    def to_representation(self, instance: RmStoreLocation):
        data = super().to_representation(instance)
        StoreList = RmStoreLocation.objects.filter(rm_id=instance.rm_id).values()
        store_data = list(StoreList)
        for store_item in store_data:
            data.update(store_item)
        return data
    
    def create(self, validated_data):
        del_rm_image = validated_data.pop('del_rm_image',False)

        rm_row_no = validated_data.pop('rm_row_no', None)
        rm_rack_no = validated_data.pop('rm_rack_no', None)
        rm_shelf_no = validated_data.pop('rm_shelf_no', None)
        rm_tub_no = validated_data.pop('rm_tub_no', None)
        remark = validated_data.pop('remark', None)

        rm_image = validated_data.pop('rm_image_uploads',None)

        requestuser = self.context['request'].user
        validated_data['create_by'] = requestuser.id
        validated_data['created_date'] = timezone.now()
        validated_data['rm_mat_desc'] = str(validated_data.get(
            'rm_mat_name')+' '+validated_data.get('rm_sec_type', ' ')+' '+validated_data.get('rm_size', ' '))
        max_rm_mat_code = RawMaterialMaster.objects.all().aggregate(Max('rm_id'))[
            'rm_id__max']

        # Increment by 1 if not None, else set to 1
        rm_mat_code_id = int(max_rm_mat_code) +  1 if max_rm_mat_code is not None else 1
        validated_data['rm_mat_code'] = rm_mat_code_id

        # rm = super().create(validated_data)
        
        instance = super().create(validated_data)
        last_inserted_id = instance.rm_id  # or instance.pk


        get_instance=RawMaterialMaster.objects.get(rm_id=last_inserted_id)
        fs = FileSystemStorage()
        if rm_image is not None and len(rm_image) != 0:
            filename = fs.save(f"Uploads/RowMaterial/Rmimages/{str(last_inserted_id)}_{rm_image}", rm_image)
            rm_image_url = fs.url(filename)
            validated_data['rm_image'] = rm_image_url
        rm_final = super().update(get_instance,validated_data)
        StockMaster.objects.create(
            rm=instance,last_update=timezone.now(),updt_by=requestuser.id,type=2
        )
        print("rm final ============ ",rm_final)
        serializer = Rm_Store_Location(data={"rm":last_inserted_id,"rm_row_no":rm_row_no,"rm_rack_no":rm_rack_no,"rm_shelf_no":rm_shelf_no,"rm_tub_no":rm_tub_no,"remark":remark})
        if serializer.is_valid():
            serializer.save()
        else:
            print(serializer.errors)
    
        return rm_final
    
    def update(self, instance:RawMaterialMaster, validated_data):
        rmId = instance.rm_id
        rm_row_no = validated_data.pop('rm_row_no', None)
        rm_rack_no = validated_data.pop('rm_rack_no', None)
        rm_shelf_no = validated_data.pop('rm_shelf_no', None)
        rm_tub_no = validated_data.pop('rm_tub_no', None)
        remark = validated_data.pop('remark', None)
        rm_image = validated_data.pop('rm_image_uploads',None)
        pkid = str(instance.rm_id)
        print("rm_image ======= ",rm_image)
        requestuser = self.context['request'].user
        validated_data['modify_by'] = requestuser.id
        validated_data['modify_date'] = timezone.now()
        # validated_data['rm_mat_desc'] = f"""{validated_data.get('rm_mat_name', instance.rm_mat_name)} {validated_data.get(
        #     'rm_sec_type', instance.rm_sec_type)} {validated_data.get('rm_size', instance.rm_size)}"""

        del_rm_image = validated_data.pop('del_rm_image',False)

        print("del_rm_image ======= ",del_rm_image)
        if del_rm_image:
            cp = os.getcwd()
            if instance.rm_image is not None:
                p = str(cp + instance.rm_image)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                print("path========",p)
                try:
                    os.remove(p)
                    print("remove done")
                except Exception as e:
                    print("delete img error :", e)
                instance.rm_image = None
                instance.save()

        if rm_image:
                rm_image_file_path = instance.rm_image
                print("rm_image_file_path ======= ",rm_image_file_path)
                if(rm_image_file_path is not None):
                    rm_image_file_path= str(os.getcwd()+rm_image_file_path)
                    if os.path.exists(rm_image_file_path):
                        try:
                            os.remove(rm_image_file_path)
                        except Exception as e:
                            print("file delete error ==> ",e)
                
                
                fs = FileSystemStorage()
                filename = fs.save(f"Uploads/RowMaterial/Rmimages/{pkid}_{rm_image}", rm_image)
                rm_url=fs.url(filename)
                # print("============= upadte rm_datasheet_file_path ============= ")
                # validated_data['rm_image']=rm_url
                print(rm_url)
                instance.rm_image=rm_url
                    # print("hiiiiiii ======= ",validated_data['rm_image_uploads'])

                # fs = FileSystemStorage()
                # filename = fs.save(f"Uploads/RowMaterial/Rmimages/{pkid}_{rm_image}", rm_image)
                # rm_url=fs.url(filename)
                # validated_data['rm_image_uploads']=rm_url


        rmHas = RmStoreLocation.objects.filter(rm=rmId).exists()
        if not rmHas:
            serializer = Rm_Store_Location(data={"rm":rmId,"rm_row_no":rm_row_no,"rm_rack_no":rm_rack_no,"rm_shelf_no":rm_shelf_no,"rm_tub_no":rm_tub_no,"remark":remark})
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)
        else:
            rm_loc_instance=RmStoreLocation.objects.get(rm=rmId)
            serializer = Rm_Store_Location(data={"rm":rmId,"rm_row_no":rm_row_no,"rm_rack_no":rm_rack_no,"rm_shelf_no":rm_shelf_no,"rm_tub_no":rm_tub_no,"remark":remark},instance=rm_loc_instance)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        return super().update(instance, validated_data)

class Raw_VendorSerializers(serializers.ModelSerializer):
    rm_vendor_datasheet_uploads = serializers.FileField(write_only=True,required=False)
    catalog_uploads = serializers.FileField(write_only=True,required=False)
    quotation_uploads = serializers.FileField(write_only=True,required=False)

    del_datasheet = serializers.BooleanField(
        default=False, required=False, write_only=True)
    del_catalog = serializers.BooleanField(
        default=False, required=False, write_only=True)     
    del_quotation = serializers.BooleanField(
        default=False, required=False, write_only=True)
    class Meta:
        model = RmVendorMaster
        exclude = []
        extra_kwargs = {
            "rm_vendor_lead_time":{
                "required": False
            },
            "rm_vendor_datasheet_url":{
                "required": False
            },
            "catalog_url":{
                "required": False
            },
            "quotation_url":{
                "required": False
            }
        }

    def to_representation(self, instance:RmVendorMaster):
        data = super().to_representation(instance)
        data['vendor_name'] = instance.vendor.vendor_name
        data['vendor_city'] = instance.vendor.vendor_city
        data['vendor_email'] = instance.vendor.vendor_email
        data['vendor_address'] = instance.vendor.vendor_address
        data['vendor_mobile'] = instance.vendor.vendor_mobile
        data['rm_mat_name'] = instance.rm.rm_mat_name
        data['rm_mat_code'] = instance.rm.rm_mat_code
        data['rm_mat_desc'] = instance.rm.rm_mat_desc
        data['rm_cost'] = instance.rm.rm_cost
        data['rm_sec_type'] = instance.rm.rm_sec_type
        data['rm_size'] = instance.rm.rm_size
      
        print(instance,"*****************")
        # print(data)
        return data 

    def create(self, validated_data):
        del_datasheet = validated_data.pop('del_datasheet',False)
        del_catalog = validated_data.pop('del_catalog',False)
        del_quotation = validated_data.pop('del_quotation',False)

        rm_vendor_datasheet = validated_data.pop('rm_vendor_datasheet_uploads',None)
        catalog_url = validated_data.pop('catalog_uploads',None)
        quotation_url = validated_data.pop('quotation_uploads',None)
        # Extract vendor ID
        instance = super().create(validated_data)
        print("intence===========",instance)
        last_inserted_id = instance.id  # or instance.pk
        print("last_inserted_id==========",last_inserted_id)
        print("validated_data============",validated_data)


        get_instance=RmVendorMaster.objects.get(id=last_inserted_id)
        fs = FileSystemStorage()
        # Process rm_vendor_datasheet
        if rm_vendor_datasheet is not None and len(rm_vendor_datasheet) != 0:
            filename = fs.save(f"Uploads/RowMaterial/RmVendor/{str(last_inserted_id)}_{rm_vendor_datasheet}", rm_vendor_datasheet)
            rm_image_url = fs.url(filename)
            validated_data['rm_vendor_datasheet_url'] = rm_image_url

        # Process catalog_url
        if catalog_url is not None and len(catalog_url) != 0:
            filename = fs.save(f"Uploads/RowMaterial/RmVendor/{str(last_inserted_id)}_{catalog_url}", catalog_url)
            cat_url = fs.url(filename)
            validated_data['catalog_url'] = cat_url

        # Process quotation_url
        if quotation_url is not None and len(quotation_url) != 0:
            filename = fs.save(f"Uploads/RowMaterial/RmVendor/{str(last_inserted_id)}_{quotation_url}", quotation_url)
            q_url = fs.url(filename)
            validated_data['quotation_url'] = q_url
        return super().update(get_instance,validated_data)
    
    def update(self, instance:RmVendorMaster, validated_data):
        rm_vendor_datasheet = validated_data.pop('rm_vendor_datasheet_uploads',None)
        catalog_url = validated_data.pop('catalog_uploads',None)
        quotation_url = validated_data.pop('quotation_uploads',None)
        pkid = str(instance.id)
        print(rm_vendor_datasheet,catalog_url,quotation_url)
        print(validated_data)  

        del_datasheet = validated_data.pop('del_datasheet',False)
        del_catalog = validated_data.pop('del_catalog',False)
        del_quotation = validated_data.pop('del_quotation',False)

        print("del_datasheet= =========",del_datasheet)
        print("del_cat= =========",del_catalog)
        print("del_quotaiion= =========",del_quotation)

        pkid = str(instance.id)        
        if del_datasheet:
            cp = os.getcwd()
            if instance.rm_vendor_datasheet_url is not None:
                p = str(cp + instance.rm_vendor_datasheet_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                print("path========",p)
                try:
                    os.remove(p)
                    print("remove done")
                except Exception as e:
                    print("delete del_datasheet img error :", e)
                instance.rm_vendor_datasheet_url = None
                instance.save()
        if del_catalog:
            cp = os.getcwd()
            if instance.catalog_url is not None:
                p = str(cp + instance.catalog_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                print("path========",p)
                try:
                    os.remove(p)
                    print("remove done")
                except Exception as e:
                    print("delete del_catalog img error :", e)
                instance.catalog_url = None
                instance.save()

        if del_quotation:
            cp = os.getcwd()
            if instance.quotation_url is not None:
                p = str(cp + instance.quotation_url)
                p = p.replace('\\', '/')
                p = p.replace('%20', ' ')
                p = p.replace('%40', '@')
                print("path========",p)
                try:
                    os.remove(p)
                    print("remove done")
                except Exception as e:
                    print("delete del_catalog img error :", e)
                instance.quotation_url = None
                instance.save()


        if rm_vendor_datasheet:
                rm_datasheet_file_path = instance.rm_vendor_datasheet_url
                if rm_datasheet_file_path is not None:
                    rm_datasheet_file_path= str(os.getcwd()+rm_datasheet_file_path)
                    if os.path.exists(rm_datasheet_file_path):
                        try:
                            os.remove(rm_datasheet_file_path)
                        except Exception as e:
                            print("file delete error ==> ",e)
                
                
                    fs = FileSystemStorage()
                    filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{rm_vendor_datasheet}", rm_vendor_datasheet)
                    rm_vondor=fs.url(filename)
                    # print("============= upadte rm_datasheet_file_path ============= ")
                    validated_data['rm_vendor_datasheet_url']=rm_vondor

                fs = FileSystemStorage()
                filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{rm_vendor_datasheet}", rm_vendor_datasheet)
                rm_vendor=fs.url(filename)
                validated_data['rm_vendor_datasheet_url']=rm_vendor

        if catalog_url:
                catalog_url_file_path = instance.catalog_url
                if catalog_url_file_path is not None:
                    catalog_url_file_path= str(os.getcwd()+catalog_url_file_path)
                    if os.path.exists(catalog_url_file_path):
                        try:
                            os.remove(catalog_url_file_path)
                            # print("============= remove catalog_url_file_path ============= ")
                        except Exception as e:
                            print("file delete error ==> ",e)
                
                
                    fs = FileSystemStorage()
                    filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{catalog_url}", catalog_url)
                    # print("============= upadte catalog_url_file_path ============= ")
                    c_url=fs.url(filename)
                    validated_data['catalog_url']=c_url
                fs = FileSystemStorage()
                filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{catalog_url}", catalog_url)
                c_url=fs.url(filename)
                validated_data['catalog_url']=c_url

        if quotation_url:
                quotation_url_file_path = instance.quotation_url
                if quotation_url_file_path is not None:
                    quotation_url_file_path= str(os.getcwd()+quotation_url_file_path)
                    if os.path.exists(quotation_url_file_path):
                        try:
                            os.remove(quotation_url_file_path)
                            # print("============= remove quotation_url_file_path ============= ")
                        except Exception as e:
                            print("file delete error ==> ",e)
                
                
                    fs = FileSystemStorage()
                    filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{quotation_url}", quotation_url)
                    # print("============= upadte quotation_url_file_path ============= ")
                    q_url=fs.url(filename)
                    validated_data['quotation_url']=q_url

                fs = FileSystemStorage()
                filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{quotation_url}", quotation_url)
                q_url=fs.url(filename)
                validated_data['quotation_url']=q_url
        
        return super().update(instance, validated_data)
        
        # if rm_vendor_datasheet:
        #         rm_datasheet_file_path = instance.rm_vendor_datasheet_url
        #         rm_datasheet_file_path= str(os.getcwd()+rm_datasheet_file_path)
        #         print("============ rm_datasheet_file_path =============",rm_datasheet_file_path)
        #         if os.path.exists(rm_datasheet_file_path):
        #             try:
        #                 os.remove(rm_datasheet_file_path)
        #                 print("remove rm_datasheet_file_path")
        #             except Exception as e:
        #                 print("file delete error ==> ",e)
              
               
        #         fs = FileSystemStorage()
        #         filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{rm_vendor_datasheet}", rm_vendor_datasheet)
        #         rm_url=fs.url(filename)
        #         # print("============= upadte rm_datasheet_file_path ============= ")
        #         validated_data['rm_vendor_datasheet_url']=rm_url

        # if catalog_url:
        #         catalog_url_file_path = instance.catalog_url
        #         catalog_url_file_path= str(os.getcwd()+catalog_url_file_path)
        #         if os.path.exists(catalog_url_file_path):
        #             try:
        #                 os.remove(catalog_url_file_path)
        #                 # print("============= remove catalog_url_file_path ============= ")
        #             except Exception as e:
        #                 print("file delete error ==> ",e)
              
               
        #         fs = FileSystemStorage()
        #         filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{catalog_url}", catalog_url)
        #         # print("============= upadte catalog_url_file_path ============= ")
        #         c_url=fs.url(filename)
        #         validated_data['catalog_url']=c_url

        # if quotation_url:
        #         quotation_url_file_path = instance.quotation_url
        #         quotation_url_file_path= str(os.getcwd()+quotation_url_file_path)
        #         if os.path.exists(quotation_url_file_path):
        #             try:
        #                 os.remove(quotation_url_file_path)
        #                 # print("============= remove quotation_url_file_path ============= ")
        #             except Exception as e:
        #                 print("file delete error ==> ",e)
              
               
        #         fs = FileSystemStorage()
        #         filename = fs.save(f"Uploads/RowMaterial/RmVendor/{pkid}_{quotation_url}", quotation_url)
        #         # print("============= upadte quotation_url_file_path ============= ")
        #         q_url=fs.url(filename)
        #         validated_data['quotation_url']=q_url
        # return super().update(instance, validated_data)



# class Mat_rtn_store_Serializer(serializers.ModelSerializer):
#     class Meta:
#           model=MatRetnStorDetail
#           exclude=[]
#     def create(self, validated_data):
#          return super().create(validated_data)

#     def update(self, instance, validated_data):
#          return super().update(instance, validated_data)
# class Mat_rtn_store_Serializer(serializers.ModelSerializer):
#     part_list = serializers.CharField(required=False,write_only=True,default="[]")
#     partdelete_list= serializers.CharField(required=False,write_only=True,default="[]")
#     class Meta:
#             model=MatRetnStorMaster
#             exclude=[]
#             extra_kwargs = {

#             "created_date":{
#                 "required":False
#             },
#             "create_by":{
#                 "required":False
#             },

#         }
#     def to_representation(self, instance:MatRetnStorMaster):
#         data=  super().to_representation(instance)


#         part_list = MatRetnStorDetail.objects.filter(mat_retn_stor=instance.mat_retn_stor_id).values(
#             'part',  # Assuming you have a field 'part_id' in PurchDetails
#             'description',
#             'mat_retn_str_det_id',
#             'uom',
#             'ref_no',
#             'rtn_qty',
#             'ioa_no',
#             product_part_no=F('part__product_part_no'),
#             product_part_name=F('part__product_part_name'),
#             product_cost=F('part__product_cost'),
#             product_descp=F('part__product_descp'),
#         )
#         data['part_list']=part_list
#         return data
#     def create(self, validated_data):
#         user_request = self.context['request'].user
#         validated_data['created_date']=timezone.now()
#         validated_data['create_by']=user_request.id
#         partlist=validated_data.get('part_list')
#         print(validated_data)
#         validated_data.pop('part_list',None)
#         validated_data.pop('partdelete_list',None)
#         mrs=super().create(validated_data)
#         mrsObj=MrsMaster.objects.get(mrs_id=mrs.mrs_id)

#         print(partlist)
#         if partlist is not None:
#             try:
#                 decoded_part_list = json.loads(partlist)
#                 print(decoded_part_list)
#                 for part in decoded_part_list:
#                     part['mrs']=mrsObj.mrs_id
#                     print("part=>",part)
#                     serializer=MrsDetailSerializer(data=part)
#                     if serializer.is_valid():
#                          serializer.save()
#                     else:
#                         print(serializer.errors)


#             except json.JSONDecodeError as e:
#                     print("partlist json: ",e)


#         return super().update(mrsObj,validated_data)
