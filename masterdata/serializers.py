from inventory_and_stores.models import StockMaster
from .models import *
from django.utils import timezone
from django.db import transaction
from django.db.models import Q, F   
from rest_framework import serializers


class InspectionSerailizer(serializers.ModelSerializer):
    class Meta:
        model = InspectionTypeMaster
        exclude = []

class ToolsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = ToolsMaster
        exclude = []
        extra_kwargs={
             "slug":{'required':False}
        }
    def validate_tool_name(self, value):
        # print("tool==>",value)
        instance = self.instance  # Get the current assemblies instance being updated
        if instance is not None and str(instance.tool_name).strip() == str(value).strip():
            return value  # a_no not changed, no need to perform validation

        if ToolsMaster.objects.filter(tool_name=value).exists():
                raise serializers.ValidationError('Tool name is a already used.')
      
        return value
    def create(self, validated_data):
        requestUser=self.context.get('request').user 
        validated_data['created_date']=timezone.now()
        validated_data['modify_by']=requestUser.id
        validated_data['created_by']=requestUser.id
        validated_data['modify_date']=timezone.now()
        return super().create(validated_data)
    def update(self, instance:ToolsMaster, validated_data):        
        request_user = self.context.get('request').user
        instance.tool_name = validated_data.get('tool_name', instance.tool_name)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.is_remove = validated_data.get('is_remove', instance.is_remove)
        instance.modify_date = timezone.now()
        instance.modify_by = request_user.id
        instance.save()
        return instance
class QC_DetailsSerailizer(serializers.ModelSerializer):
    qcd_id=serializers.IntegerField(required=False)
    class Meta:
        model = QcDetails
        exclude = []
        extra_kwargs = {
            "qc": {"required": False},
            }
class QC_Serializer(serializers.ModelSerializer):
    qc_details = QC_DetailsSerailizer(many=True, required=True, write_only=True)
    del_qcd=serializers.ListField(required=False,write_only=True)
    class Meta:
        model = QcMaster
        exclude = []
        extra_kwargs = {
            
            "qc_no": {"required": False},
            "created_date": {"required": False},
            "created_by": {"required": False},
            "modify_by": {"required": False},
            "modify_date": {"required": False},
            "is_remove": {"default": False}
        }

    def to_representation(self, instance:QcMaster):
        data=super().to_representation(instance)
        data['part_no']=instance.part.product_part_no
        data['part_name']=instance.part.product_part_name
        qc_details=QcDetails.objects.filter(qc_id=instance.qc_id).values(
            'parameter_name','nominal_dimension','tolerance_positive','tolerance_negative','tolerance_tool_other','uom','qc','qcd_id','inspt_type',tolerance_tool_other_name=F('tolerance_tool_other__tool_name'),inspt_type_name=F('inspt_type__inspt_name')
        )
        data['qc_details']=qc_details
        return data 
    def validate_qc_details(self, value):
        if not value:
            raise serializers.ValidationError("Qc_details cannot be empty.")
        return value
    def generate_no(self):
        # Extract PO number generation into its own method
        initial_offset = 1
        total_count = QcMaster.objects.count()
        new_no = total_count + initial_offset
        return 'QC{:04d}'.format(new_no)

    @transaction.atomic
    def create(self, validated_data):
        request_user=self.context.get('request').user

        validated_data['qc_no']=self.generate_no()
        validated_data['created_date']=timezone.now()
        validated_data['modify_date']=timezone.now()
        validated_data['modify_by']=request_user.id
        validated_data['created_by']=request_user.id
        qc_details_data = validated_data.pop('qc_details')
        del_qcd = validated_data.pop('del_qcd',[])
        qc_master_instance = super().create(validated_data)
        self._create_qc_details(qc_master_instance, qc_details_data)
        return qc_master_instance

    @transaction.atomic
    def update(self, instance, validated_data):
        request_user=self.context.get('request').user
        qc_details_data = validated_data.pop('qc_details')
        validated_data['modify_date']=timezone.now()
        validated_data['modify_by']=request_user.id
        del_qcd = validated_data.pop('del_qcd',[])
        if del_qcd:
            QcDetails.objects.filter(qcd_id__in=del_qcd).delete()
        instance = super().update(instance, validated_data)
        self._update_qc_details(instance, qc_details_data)
        return instance

    def _create_qc_details(self, qc_master_instance, qc_details_data):
        for qc_detail_data in qc_details_data:
            QcDetails.objects.create(qc=qc_master_instance, **qc_detail_data)

    def _update_qc_details(self, qc_master_instance, qc_details_data):
        for qc_detail_data in qc_details_data:
            qc_detail_id = qc_detail_data.get('qcd_id')
            if qc_detail_id:
                qc_detail_instance = QcDetails.objects.get(qcd_id=qc_detail_id, qc=qc_master_instance)
                for attr, value in qc_detail_data.items():
                    setattr(qc_detail_instance, attr, value)
                qc_detail_instance.save()
            else:
                QcDetails.objects.create(qc=qc_master_instance, **qc_detail_data)
    

class PartBoughtOutSerailizer(serializers.ModelSerializer):
    class Meta:
        model=PartsMaster
        fields=['part_id','product_part_no','product_part_name','product_descp','product_type','category','source']
    def to_representation(self, instance: PartsMaster):
        representation = super().to_representation(instance)
        product_category = instance.category
        category_name = getattr(product_category, 'c_name', None)
        if instance.source:
             representation['source_name']=instance.source.s_name
        if StockMaster.objects.filter(part=instance.part_id).exists():
            stock_avail=StockMaster.objects.get(part=instance.part_id)
            
            representation['stock_avail'] = int(stock_avail.stock_avail) if stock_avail.stock_avail is not None else 0
        else:
                            representation['stock_avail'] = 0
        representation['product_category_name'] = category_name

        return representation