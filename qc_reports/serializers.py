import json

from inventory_and_stores.models import StoreLocation
from .models import *
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, F 
from django.db.models import Prefetch  
from masterdata.models import *
from rest_framework import serializers
class QCReportMeasuedSerializer(serializers.ModelSerializer):
    qcm_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = QcReportsMeasued
        exclude = []
        extra_kwargs={
            "qcrd":{"required":False}
        }


class QCReportDetailsSerializer(serializers.ModelSerializer):
    qcrd_id = serializers.IntegerField(required=False)
    measured_list = QCReportMeasuedSerializer(many=True)
    class Meta:
        model = QcReportsDetails
        exclude = []
        extra_kwargs={
            "qcr":{"required":False}
        }
 

    
class QCReportSerializer(serializers.ModelSerializer):
    qcr_details=QCReportDetailsSerializer(many=True,write_only=True)
    del_measured_list=serializers.ListField(required=False)

    class Meta:
        model=QcReportsMaster
        exclude=['is_delete']
        extra_kwargs={
            "created_date":{"required":False},
            "created_by":{"required":False},
            "modify_date":{"required":False},
            "qcr_no":{"required":False},
            "modify_by":{"required":False},
        }
    def validate_qcr_details(self, value):
        if not value:
            raise serializers.ValidationError("Qcr_details cannot be empty.")
        return value
    def generate_qcr_no(self):
        # Extract PO number generation into its own method
        initial_offset = 1
        total_count = QcReportsMaster.objects.count()
        new_no = total_count + initial_offset
        return 'QCR{:04d}'.format(new_no) 
  
    def to_representation(self, instance: QcReportsMaster):
        data = super().to_representation(instance)

        # Fetch related part information using join query
        
        print(instance.part,"oooooooooooooo")
        part_info = instance.part
        if part_info:
            data['product_part_no'] = part_info.product_part_no
            data['product_part_name'] = part_info.product_part_name
            data['product_cost'] = part_info.product_cost
            data['product_descp'] = part_info.product_descp
            source_info = part_info.source
            if source_info:
                data['source_name'] = source_info.s_name
                data['source_id'] = source_info.id
            category_info = part_info.category
            if category_info:
                data['category_name'] = category_info.c_name
                data['category_id'] = category_info.category_id
            if StoreLocation.objects.filter(part=part_info).exists():
                partstoreloc=StoreLocation.objects.filter(part=part_info).first()
                data['store_loc_row_no']=partstoreloc.row_no
                data['store_loc_rack_no']=partstoreloc.rack_no
                data['store_loc_shelf_no']=partstoreloc.shelf_no
                data['store_loc_tub_no']=partstoreloc.tub_no
                data['store_loc_remark']=partstoreloc.remark


        vendor_info = instance.vendor
        if vendor_info:
            data['vendor_id'] = vendor_info.vendor_id
            data['vendor_name'] = vendor_info.vendor_name
            data['vendor_email'] = vendor_info.vendor_email
            data['vendor_city'] = vendor_info.vendor_city
            data['vendor_address'] = vendor_info.vendor_address
        qc_format = (QcReportsDetails.objects
                             .filter(qcr=instance)
                             .annotate(qc_no=F('qcd__qc__qc_no'))
                             .values('qc_no')
                             .distinct().first())
        # print(qc_format)
        if qc_format:
            data['qc_no']=qc_format.get('qc_no')
        # Fetch related QcReportsDetails information using join query
        qcr_details = QcReportsDetails.objects.filter(qcr=instance).values(
            'qcrd_id', 'qc_id', 'qcd_id', 'qcr','status',
            qc_no=F('qcd__qc__qc_no'),
            product_part_no=F('qcd__qc__part__product_part_no'),
            product_part_name=F('qcd__qc__part__product_part_name'),
            category=F('qcd__qc__part__category__c_name'),
            source=F('qcd__qc__part__source__s_name'),
            product_descp=F('qcd__qc__part__product_descp'),
            product_cost=F('qcd__qc__part__product_cost'),
            part_id=F('qcd__qc__part_id'),
            parameter_name=F('qcd__parameter_name'),
            nominal_dimension=F('qcd__nominal_dimension'),
            tolerance_positive=F('qcd__tolerance_positive'),
            tolerance_negative=F('qcd__tolerance_negative'),
            tolerance_other=F('qcd__tolerance_tool_other__tool_name'),
            uom=F('qcd__uom'),
            inspt_type=F('qcd__inspt_type_id'),
            inspt_type_name=F('qcd__inspt_type__inspt_name'),
        )

        # Fetch related QcReportsMeasured information using join query
        for qcrd in qcr_details:
            qcrd['measured_list'] = list(QcReportsMeasued.objects.filter(qcrd=qcrd['qcrd_id']).values())

        data['qcr_details'] = list(qcr_details)

        return data
   
    
    @transaction.atomic
    def create(self, validated_data):
        
        request_user = self.context.get('request').user
        qcr_details_data = validated_data.pop('qcr_details', [])
        validated_data.pop('del_measured_list',None)
        validated_data['qcr_no'] = self.generate_qcr_no()
        validated_data['created_by'] = request_user.id
        validated_data['modify_by'] = request_user.id
        validated_data['modify_date'] = timezone.now()
        validated_data['created_date'] = timezone.now()

        qc_report = QcReportsMaster.objects.create(**validated_data)
        for qcr_details_item in qcr_details_data:
            qcr_details_item['qcr']=qc_report
            measured_list_data = qcr_details_item.pop('measured_list', [])
            qcr_details = QcReportsDetails.objects.create(**qcr_details_item)
            for measured_data in measured_list_data:
                QcReportsMeasued.objects.create(qcrd=qcr_details, **measured_data)
        return qc_report
    
    def update(self, instance, validated_data):
        request_user = self.context.get('request').user
        qcr_details_data = validated_data.pop('qcr_details', [])
        del_measured_list=validated_data.pop('del_measured_list',None)
        if del_measured_list:
            QcReportsMeasued.objects.filter(qcm_id__in=del_measured_list).delete()
  
        validated_data['modify_by'] = request_user.id
        validated_data['modify_date'] = timezone.now()
        
        for qcr_details_item in qcr_details_data:
            qcr_details_item['qcr']=instance
            measured_list_data = qcr_details_item.pop('measured_list', [])
            print(qcr_details_item.get('qcrd_id'),qcr_details_item)
            qcrd_id=qcr_details_item.pop('qcrd_id',None)
            qcr_details = QcReportsDetails.objects.filter(qcrd_id=qcrd_id).update(**qcr_details_item)
            for measured_data in measured_list_data:
                print(measured_data.get('qcm_id'),measured_data)

                if measured_data.get('qcm_id'):
                    qcm_id=measured_data.pop('qcm_id',None)
                    QcReportsMeasued.objects.filter(qcm_id=qcm_id).update(**measured_data)
                else:
                    qcr_detail_instance=QcReportsDetails.objects.get(qcrd_id=qcrd_id)
                    QcReportsMeasued.objects.create(qcrd=qcr_detail_instance, **measured_data)

        return super().update(instance,validated_data)
        