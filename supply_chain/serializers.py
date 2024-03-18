from rest_framework import serializers
from django.core.files.storage import FileSystemStorage
from datetime import datetime, date
from django.utils import timezone
from inventory_and_stores.models import PartsVendorsMaster,RmVendorMaster,RmStoreLocation
from notification.models import Notification
from .models import *
import os
from django.db.models import Q, F   
from vekaria_erp.settings import MEDIA_ROOT
from django.db.models import Max
import json
from django.db import transaction
from rest_framework.exceptions import ValidationError
from .utils import Utils

from authuser.models import AuthUser, UserApproval

class PR_DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrProcessDetails
        exclude = []
        extra_kwargs={
            "prp":{
                "required": False
            }
        }


class PR_UserApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApproval
        exclude = []
        extra_kwargs={
         
        }
    def to_representation(self, instance:UserApproval):
        data= super().to_representation(instance)
        if instance.user:
            data['username']=instance.user.username
            data['first_name']=instance.user.first_name
            data['last_name']=instance.user.last_name
            data['email']=instance.user.email
        return data

class PR_ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchRequistion
        fields = ['pr_status','remarks']
        extra_kwargs = {
            "pr_status": {
                "required": True
            },
            "remarks": {
                "required": True
            }
        }

    def update_notifications_to_read(self, status, user_id, pr_id):
        notification=Notification.objects.filter(
            type=status, receiver_user=user_id, action=pr_id
        )
        for notifi in notification:
            notifi.is_read=True
            notifi.save()

    def create_notification(self, type, message, receiver_user, sender_user_id, pr_id):
        Notification.objects.create(
            type=type,
            message=message,
            created_date=timezone.now(),
            receiver_user=receiver_user,
            sender_user_id=sender_user_id,
            action=pr_id,
            is_read=False
        )

    def validate_user_approval(self, user_id, approver_level):

        user_approval = UserApproval.objects.filter(user=user_id).first()
        if not user_approval or user_approval.approver_level != approver_level:
            raise ValidationError({"message": "You do not have permission to perform this action."})
        return user_approval

    def handle_approval(self, instance:PurchRequistion, validated_data, request_user):
        pr_status = validated_data.get('pr_status')
        user_approval = UserApproval.objects.filter(user=request_user.id).first()

        if pr_status in ['PR_APPROVED', 'PR_RETURN', 'PR_REJECTED']:
            # print(pr_status)
            self.update_notifications_to_read('PR_Approval', request_user.id, instance.pr_id)

        if pr_status == 'PR_APPROVED':
            self.process_approval(instance, request_user, validated_data,user_approval)
        elif pr_status == 'PR_RETURN':
            self.process_return(instance, request_user, validated_data)
        elif pr_status == 'PR_REJECTED':
            # Assuming rejection logic is similar for both levels
            # Adjust as per your application's requirements
            notification_message = f"A purchase requisition with the code {instance.pr_no} has been rejected."
            if instance.pr_approval_level==2 and instance.pr_lvl_1_approved:
                notification_user = AuthUser.objects.filter(id=instance.pr_approval_lvl_1_users)
                if notification_user.exists():
                    self.create_notification("INFO",notification_message,notification_user[0],request_user.id,instance.pr_id)

            # create by user 
            notification_user = AuthUser.objects.filter(id=instance.pr_create_by)
            if notification_user.exists():
                self.create_notification("INFO",notification_message,notification_user[0],request_user.id,instance.pr_id)

        else:
            raise ValidationError({"message": "Invalid PR status."})

    def process_approval(self, instance:PurchRequistion, request_user, validated_data,user_approval:UserApproval):
        if instance.pr_approval_level == 1:
           if int(request_user.id) == instance.pr_approval_lvl_1_users:
                validated_data['pr_lvl_1_approved'] = True
               
        elif instance.pr_approval_level == 2  :
            # approval lvl 1 user approved
            if not instance.pr_lvl_1_approved  and int(request_user.id) == instance.pr_approval_lvl_1_users:
                validated_data['pr_lvl_1_approved'] = True
                validated_data.pop('pr_status')

                if instance.pr_approval_lvl_2_users :
                        notification_user = AuthUser.objects.filter(id=instance.pr_approval_lvl_2_users)
                        # print(notification_user)
                        notification_message=f"A purchase requisition with the code {instance.pr_no} has been generated. Please click here to approve the PR."  
                        if notification_user.exists():
                            self.create_notification(
                            type='PR_Approval',
                            message=notification_message,
                            receiver_user=notification_user[0],
                            sender_user_id=instance.pr_create_by,
                            pr_id=instance.pr_id
                        )
                

            # approval lvl 2 user approved
            elif not instance.pr_lvl_2_approved and instance.pr_lvl_1_approved and int(request_user.id) == instance.pr_approval_lvl_2_users:
                validated_data['pr_lvl_2_approved'] = True
               
            else:
                raise ValidationError({"message": "You do not have permission to perform this action."})


    def process_return(self, instance:PurchRequistion, request_user, validated_data):
        receiver_notification_user = AuthUser.objects.filter(id=instance.pr_create_by).first()
        if not receiver_notification_user:
            raise ValidationError({"message": "Invalid PR creator."})

        notification_message = f"A purchase requisition with the code {instance.pr_no} has been returned. Please click here to update it."
        self.create_notification(
            type='PR_Return',
            message=notification_message,
            receiver_user=receiver_notification_user,
            sender_user_id=request_user.id,
            pr_id=instance.pr_id
        )
        notification_message = f"A purchase requisition with the code {instance.pr_no} has been returned."

        if instance.pr_approval_level==2 and instance.pr_lvl_1_approved:
                notification_user = AuthUser.objects.filter(id=instance.pr_approval_lvl_1_users)
                if notification_user.exists():
                    self.create_notification("INFO",notification_message,notification_user[0],request_user.id,instance.pr_id)


    def update(self, instance:PurchRequistion, validated_data):
        with transaction.atomic():
            request_user = self.context['request'].user
            approver_level = instance.pr_approval_level
            # print( request_user.is_superuser)
            # if not request_user.is_superuser:
            #     print("yes")
            # # Validate if the request user has approval rights
            #     self.validate_user_approval(request_user.id, approver_level)

            # Handle the approval based on the PR status
            self.handle_approval(instance, validated_data, request_user)

            return super().update(instance, validated_data)



class PartListSerializer(serializers.Serializer):
    rfqd_id=serializers.PrimaryKeyRelatedField(queryset=RfqDetails.objects.all(),required=False)
    part = serializers.PrimaryKeyRelatedField(queryset=PartsMaster.objects.all())
    part_qty = serializers.IntegerField()
    make= serializers.CharField(required=False)
    model= serializers.CharField(required=False)
    specification_text= serializers.CharField(required=True,allow_null=True)
      
class RFQ_Serializer(serializers.ModelSerializer):
    part_list=  serializers.ListField(child=PartListSerializer(),write_only=True,required=True )
    delpart_list= serializers.ListField(write_only=True,required=False)

    def to_representation(self, instance:RfqMaster):
        data=super().to_representation(instance)
        if instance.vendor:
            data['vendor_name']=instance.vendor.vendor_name
            data['vendor_email']=instance.vendor.vendor_email
            data['vendor_mobile']=instance.vendor.vendor_mobile
            data['vendor_city']=instance.vendor.vendor_city
        part_list = RfqDetails.objects.filter(rfq=instance).values(
                'part',                                                        
                'rfq',
                'part_qty',
                'rfqd_id',
                product_part_no=F('part__product_part_no'),
                product_part_name=F('part__product_part_name'),
                product_cost=F('part__product_cost'),
                product_descp=F('part__product_descp'),
                product_type=F('part__product_type'),
                uom=F('part__uom'),)
        data['part_list']=part_list                                                    
        return data
    class Meta:
        model=RfqMaster
        exclude=[]
        extra_kwargs={
            "rfq_no":{
                "required": False
            },
            "type":{
                "required": False
            },
           
        }
    def update(self, instance, validated_data):
        part_list=validated_data.pop('part_list')
        delpart_list=validated_data.pop('delpart_list',None)
        if delpart_list:
            RfqDetails.objects.filter(rfqd_id__in=delpart_list).delete()
        for part in part_list:
            # print(part)
            if part.get('rfqd_id'):
                rfqd_id=part.pop('rfqd_id').rfqd_id
               
                print("update rfqd====>",part)
                RfqDetails.objects.filter(rfqd_id=rfqd_id).update(**part)
            else:
                print("create ====>",part)

                RfqDetails.objects.create(rfq=instance,**part)


        return super().update(instance, validated_data)
   
class RFQ_DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=RfqDetails
        exclude=[]
    def create(self, validated_data):

        return super().create(validated_data)
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

   
class RFQ_VendorSerializer(serializers.Serializer):
    # vendor_list=serializers.CharField()
    vendor_list=RFQ_Serializer(many=True,required=True,write_only=True)

   
    def create(self, validated_data):
        # vendor_list= json.loads(validated_data['vendor_list'])
        vendor_list= validated_data['vendor_list']
        request_user = self.context['request'].user

        # serializer=RFQ_Serializer(many=True,data=vendor_list)
        # if serializer.is_valid(raise_exception=True): 
        for vendor in vendor_list:
                vendor_email=vendor['vendor'].vendor_email

                try:
                    rfq_obj = RfqMaster.objects.latest('rfq_no')
                except RfqMaster.DoesNotExist:
                    rfq_obj=None

                new_rfq_no =  1

                latest_rqf_no = rfq_obj.rfq_no if rfq_obj else None     
                if latest_rqf_no:  
                    # Increment the latest mrs_id by 1
                    current_rqf_no = int(latest_rqf_no[3:])
                    new_rfq_no = current_rqf_no + 1
                    # print(new_rfq_no)
                formatted_rfq_no= 'RFQ{:04d}'.format(new_rfq_no)
                part_list=vendor.pop('part_list')
                vendor['rfq_no']=formatted_rfq_no
                vendor['created_date']=timezone.now()
                vendor['modify_date']=timezone.now()
                vendor['created_by']=request_user.id
                vendor['modify_by']=request_user.id
                
                rfq=RfqMaster.objects.create(**vendor)
                validated_data['rfq_id']=rfq.rfq_id
                data={
                    "to_email":vendor_email,
                    "rfq_no":formatted_rfq_no,
                    "created_date":timezone.now(),
                    "subject":"RFQ Request",
                    "body":"RFQ request",
                    "logo": f"{MEDIA_ROOT}/vekaria_logo (1).png",
                    "part_list":part_list
                }
                result_email=Utils.send_vendor_email(data)
                # print(data,result_email)
                for part in part_list:
                    # spec_upload_url=None
                    # if part.get('specification_upload') is not None and len( part.get('specification_upload'))!=0:
                    #     fs = FileSystemStorage()
                    #     pic_upload_name = part.get('specification_upload').name.replace(' ', '_')
                    #     filename = fs.save(f"Uploads/RFQ/{str(formatted_rfq_no)+'_'+pic_upload_name}", part.get('specification_upload'))
                    #     spec_upload_url = fs.url(filename)
                    # part['specification_upload']=spec_upload_url
         
                    RfqDetails.objects.create(rfq=rfq,**part)

        # print(vendor_list)

        return validated_data
    


    # approval 
    # def update(self, instance:PurchRequistion, validated_data):
    #     request_user = self.context['request'].user
        
    #     if instance.pr_approval_level==1:
    #         user=UserApproval.objects.filter(user=request_user.id,approval__contain='PR',approver_level=1).first()
    #         if user.approver_level==1:
            
    #             if not instance.pr_lvl_1_approved:
    #                     lv1_user= instance.pr_approval_lvl_1_users

    #                     if int(request_user.id) == int(lv1_user):
    #                         if validated_data.get('pr_status')=='PR_APPROVED':
    #                             validated_data['pr_lvl_1_approved']=True
    #                         return super().update(instance,validated_data)
    #                     else:
    #                         raise serializers.ValidationError({"message":"You have not permission to perform this action."})

    #         else:
    #             raise serializers.ValidationError({"message":"You have not permission to perform this action."})
    #     elif instance.pr_approval_level==2:
    #         user=UserApproval.objects.filter(user=request_user.id,approval__approval_name__contain='PR').first()
    #         if user.approver_level==1:
    #                 if not instance.pr_lvl_1_approved:
    #                     lv1_user= instance.pr_approval_lvl_1_users 

    #                     if int(request_user.id) == lv1_user:
    #                         if validated_data.get('pr_status')=='PR_APPROVED':
    #                             validated_data['pr_lvl_1_approved']=True
    #                             validated_data.pop('pr_status')
    #                         return super().update(instance,validated_data)
    #                     else:
    #                         raise serializers.ValidationError({"message":"You have not permission to perform this action."})
    #         elif user.approver_level==2:
    #             if (not instance.pr_lvl_2_approved) and (instance.pr_lvl_1_approved):
    #                     lv2_user= instance.pr_approval_lvl_2_users 

    #                     if int(request_user.id) == lv2_user:
    #                         if validated_data.get('pr_status')=='PR_APPROVED':
    #                             validated_data['pr_lvl_2_approved']=True
    #                         return super().update(instance,validated_data)
    #                     else:
    #                         raise serializers.ValidationError({"message":"You have not permission to perform this action."})
    #             else:
    #                 raise serializers.ValidationError({"message":"This PR approver level 1 action is pending."})
                
    #         else:
                    
    #                 raise serializers.ValidationError({"message":"You have not permission to perform this action."})
    #     return instance


class PR_ProcessSerializer(serializers.ModelSerializer):
    PR_list = PR_DetailSerializer(many=True, write_only=True)  # Use write_only for creation
    PR_delete= serializers.ListField(required=False)
    class Meta:
        model = PrProcessMaster
        exclude = []
        extra_kwargs={
            "status":{
                "required": False
            },
            "prp_no":{
                "required": False
            }
        }
    def to_representation(self, instance:PrProcessMaster):
        data=super().to_representation(instance)
        pr_details=PrProcessDetails.objects.filter(prp=instance.prp_id).values('prpd_id','prp_id','pr_id',pr_no=F('pr_id__pr_no'),pr_date=F('pr_id__pr_date'),pr_type=F('pr_id__type')
                                                                              ,dept_name=F('pr_id__dept__dept_name'),dept=F('pr_id__dept'),req_by_date=F('pr_id__req_by_date'),
                                                                              pr_status=F('pr_id__pr_status')
                                                                              )
        for pr in pr_details:
            pr_d=PurchRequistionDetails.objects.filter(pr=pr.get('pr_id')).values(   
                'part',  
                'part_id',  
                'pr',
                'prd_id',
                'part_qty',
                'ioa_no',
                 'rm',        
            'part_qty',
            'ioa_no',    
            'type',
            rm_mat_name=F('rm__rm_mat_name'),                  
            rm_mat_code=F('rm__rm_mat_code'),                  
            rm_mat_desc=F('rm__rm_mat_desc'),                   
            rm_sec_type=F('rm__rm_sec_type'),                   
            rm_size=F('rm__rm_size'),                   
            hsn_code=F('rm__hsn_code'),                   
            rm_cost=F('rm__rm_cost'),                   
            rm_uom=F('rm__uom'),                     
            rm_image=F('rm__rm_image'),                   
            rm_drawing_no=F('rm__drawing_no'), 
                product_part_no=F('part__product_part_no'),
                product_part_name=F('part__product_part_name'),
                product_cost=F('part__product_cost'),
                product_descp=F('part__product_descp'),
                product_type=F('part__product_type'),
                uom=F('part__uom'),)
            pr['product_list']=pr_d
        data['PR_list']=pr_details
        return data
    def create(self, validated_data):
        pr_details_data = validated_data.pop('PR_list', [])
        request_user = self.context['request'].user
        try:
            l_prp_id = PrProcessMaster.objects.latest('prp_no') 
        except PrProcessMaster.DoesNotExist:
            l_prp_id=None
        
        new_prp_id =  1
        latest_prp_no = l_prp_id.prp_no if l_prp_id else None     
        if latest_prp_no:  
            # Increment the latest mrs_id by 1
            current_prp_id = int(latest_prp_no[3:])
            new_prp_id = current_prp_id + 1
         
        formatted_prp_id = 'PRP{:04d}'.format(new_prp_id)
        validated_data['prp_no']=formatted_prp_id
        validated_data['created_date'] = timezone.now()
        validated_data['created_by'] = request_user.id
        validated_data['modify_date'] = timezone.now()
        validated_data['modify_by'] = request_user.id
        validated_data['status']='PENDING'
        pr_process_master = PrProcessMaster.objects.create(**validated_data)
        for prd_data in pr_details_data:
            pr_id=prd_data.get('pr')
           
            PurchRequistion.objects.filter(pr_id=pr_id.pr_id).update(pr_status='PO_PENDING')
            PrProcessDetails.objects.create(prp=pr_process_master, **prd_data)

        return pr_process_master
    def update(self, instance:PrProcessMaster, validated_data):
        pr_details_data = validated_data.pop('PR_list', [])
        PR_delete = validated_data.pop('PR_delete', [])
        request_user = self.context['request'].user

        instance.modify_date = timezone.now()
        instance.modify_by = request_user.id
        instance.save()

        for prd_data in pr_details_data:
            pr_detail_id = prd_data.get('prpd_id')
            pr_detail_instance = PrProcessDetails.objects.get(pk=pr_detail_id) if pr_detail_id else None

            if pr_detail_instance:
                # Update existing PrProcessDetails instance
                pr_detail_instance.prp = instance
                pr_detail_instance.pr = prd_data.get('pr_id')
                pr_detail_instance.save()
            else:
                # Create a new PrProcessDetails instance
                PrProcessDetails.objects.create(prp=instance, **prd_data)

        if len(PR_delete)>0:
            PrProcessDetails.objects.filter(prpd__in=PR_delete).delete()
            

        return instance
class PoDetailSerializer(serializers.ModelSerializer):
    pod_id=serializers.IntegerField(required=False)
    class Meta:
        model = PoDetails
        exclude = []
        extra_kwargs = {
            "po": {"required": False},
             "pr_req_qty":{
                 "required": False
             },
             "status":{
                 "required": False
                 
             }
         }
   
class PO_ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PoMaster
        fields = ['status','remarks']
        extra_kwargs = {
            "status": {
                "required": True
            },
            "remarks": {
                "required": True
            }
        }
    @transaction.atomic
    def update_notifications_to_read(self, status, user_id, po_id):
        notification=Notification.objects.filter(
            type=status, receiver_user=user_id, action=po_id
        )
        for notifi in notification:
            notifi.is_read=True
            notifi.save()

    def create_notification(self, type, message, receiver_user, sender_user_id, po_id):
        Notification.objects.create(
            type=type,
            message=message,
            created_date=timezone.now(),
            receiver_user=receiver_user,
            sender_user_id=sender_user_id,
            action=po_id,
            is_read=False
        )

    def validate_user_approval(self, user_id, approver_level):
        user_approval = UserApproval.objects.filter(user=user_id).first()
        if not user_approval or user_approval.approver_level != approver_level:
            raise ValidationError({"message": "You do not have permission to perform this action."})
        return user_approval

    def handle_approval(self, instance:PoMaster, validated_data, request_user):
        po_status = validated_data.get('status')
        user_approval = UserApproval.objects.filter(user=request_user.id).first()

        if po_status in ['PO_APPROVED', 'PO_RETURN', 'PO_REJECTED']:
            # print(po_status)
            self.update_notifications_to_read('PO_Approval', request_user.id, instance.po_id)

        if po_status == 'PO_APPROVED':
            self.process_approval(instance, request_user, validated_data,user_approval)
        elif po_status == 'PO_RETURN':
            self.process_return(instance, request_user, validated_data)
        elif po_status == 'PO_REJECTED':
            notification_message = f"A purchase order with the code {instance.po_no} has been rejected."
            #lvl 1 notification
            if instance.po_approval_level==2 and instance.po_lvl_1_approved:
                notification_user = AuthUser.objects.filter(id=instance.po_approval_lvl_1_users)
                if notification_user.exists():
                    self.create_notification("INFO",notification_message,notification_user[0],request_user.id,instance.po_id)

            # create by user 
            notification_user = AuthUser.objects.filter(id=instance.po_create_by)
            if notification_user.exists():
                self.create_notification("INFO",notification_message,notification_user[0],request_user.id,instance.po_id)
            pod_list_data =PoDetails.objects.filter(po=instance.po_id)
            for pod_data in pod_list_data:
                pod = PurchRequistion.objects.filter(pr_id=pod_data.pr.pr_id).update(pr_status="PO_REJECTED")
            
        else:
            raise ValidationError({"message": "Invalid PR status."})

    def process_approval(self, instance:PoMaster, request_user, validated_data,user_approval:UserApproval):

        if instance.po_approval_level == 1:
           
           if int(request_user.id) == instance.po_approval_lvl_1_users:
                validated_data['po_lvl_1_approved'] = True
                pod_list_data =PoDetails.objects.filter(po=instance.po_id)
                for pod_data in pod_list_data:
                    pod = PurchRequistion.objects.filter(pr_id=pod_data.pr.pr_id).update(pr_status="PO_RELEASED")
            
        elif instance.po_approval_level == 2  :
            # approval lvl 1 user approved
            if not instance.po_lvl_1_approved  and int(request_user.id) == instance.po_approval_lvl_1_users:
                validated_data['po_lvl_1_approved'] = True
                validated_data.pop('status')

                if instance.po_approval_lvl_2_users:
                        notification_user = AuthUser.objects.filter(id=instance.po_approval_lvl_2_users)
                        notification_message = f"A purchase order with the code {instance.po_no} has been generated. Please click here to approve the PO."  
                        if notification_user.exists:
                            self.create_notification(
                                type='PO_Approval',
                                message=notification_message,
                                receiver_user=notification_user[0],
                                sender_user_id=instance.po_create_by,
                                po_id=instance.po_id
                            )
                

            # approval lvl 2 user approved
            elif not instance.po_lvl_2_approved and instance.po_lvl_1_approved and int(request_user.id) == instance.po_approval_lvl_2_users:
                validated_data['po_lvl_2_approved'] = True
                pod_list_data =PoDetails.objects.filter(po=instance.po_id)
                for pod_data in pod_list_data:
                    pod = PurchRequistion.objects.filter(pr_id=pod_data.pr.pr_id).update(pr_status="PO_APPROVED")
            
            else:
                raise ValidationError({"message": "You do not have permission to perform this action."})

                


    def process_return(self, instance:PoMaster, request_user, validated_data):
        receiver_notification_user = AuthUser.objects.filter(id=instance.po_create_by).first()
        if not receiver_notification_user:
            raise ValidationError({"message": "Invalid Po creator."})

        notification_message = f"A purchase order with the code {instance.po_no} has been returned. Please click here to update it."
        self.create_notification(
            type='PO_Return',
            message=notification_message,
            receiver_user=receiver_notification_user,
            sender_user_id=request_user.id,
            po_id=instance.po_id
        )
        pod_list_data =PoDetails.objects.filter(po=instance.po_id)
        for pod_data in pod_list_data:
            pod = PurchRequistion.objects.filter(pr_id=pod_data.pr.pr_id).update(pr_status="PO_RETURN")
        notification_message = f"A purchase order with the code {instance.pr_no} has been returned."

        if instance.po_approval_level==2 and instance.po_lvl_1_approved:
                notification_user = AuthUser.objects.filter(id=instance.po_approval_lvl_1_users)
                if notification_user.exists():
                    self.create_notification("INFO",notification_message,notification_user[0],request_user.id,instance.po_id)

    def update(self, instance:PoMaster, validated_data):
        with transaction.atomic():
            request_user = self.context['request'].user
            approver_level = instance.po_approval_level

            # Validate if the request user has approval rights
            # self.validate_user_approval(request_user.id, approver_level)

            # Handle the approval based on the PR status
            self.handle_approval(instance, validated_data, request_user)

            return super().update(instance, validated_data)

class PO_ReturnSerializer(serializers.ModelSerializer):
    PR_list = PoDetailSerializer(many=True,write_only=True)   
    # PO_delete_list=serializers.ListField(required=False)
    class Meta:
        model = PoMaster  
        fields =['PR_list'] 
        extra_kwargs = {
            "status": {"required": False},
                                                                                                                                                                 
       
        }

    def update_notifications_to_read(self, status, user_id, pr_id):
        notification=Notification.objects.filter(
            type=status, receiver_user=user_id, action=pr_id
        )
        for notifi in notification:
            notifi.is_read=True
            notifi.save()

    def create_notification(self, instance, user_id, approval_level):
        # Generalized method to create a notification
        message = f"A purchase order with the code {instance.po_no} has been generated. Please click here to approve the PO."
        Notification.objects.create(
            type='PO_Approval',
            message=message,
            created_date=timezone.now(),
            sender_user_id=user_id,
            receiver_user=AuthUser.objects.get(pk=user_id),
            action=instance.po_id,
            is_read=False
        )

    def update(self, instance: PoMaster, validated_data):
        with transaction.atomic():
            pr_list_data = validated_data.pop('PR_list', [])
            pr_delete_list = validated_data.pop('PO_delete_list', [])
            validated_data['status']="PO_UNDER_APPROVAL"
            requestuser = self.context['request'].user

            instance = super().update(instance, validated_data)
          
            # Efficient deletion
            # if pr_delete_list:
            #     PoDetails.objects.filter(pod_id__in=pr_delete_list).delete()

            # Pre-fetch PurchRequistionDetails
            # pr_ids = [pr_data['pr'] for pr_data in pr_list_data if 'pr' in pr_data]
            # prd_qs = PurchRequistionDetails.objects.filter(pr__in=pr_ids).annotate(pr_id=F('pr'), part_id=F('part')).values('pr_id', 'part_id', 'part_qty')
            # prd_map = {(prd['pr_id'], prd['part_id']): prd['part_qty'] for prd in prd_qs}

            # Update or create PoDetails instances
            for pr_data in pr_list_data:
                prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), part=pr_data.get('part'))
                # Set a default value if prd does not exist
                pr_data['pr_req_qty'] = prd[0].part_qty if prd.exists() else 0  # Assuming 0 is an acceptable default value
                # Update or create logic
                pod_id = pr_data.get('pod_id', None)
                # defaults = {key: value for key, value in pr_data.items()}
                # pr_data("defaults po==>",defaults)
                if pod_id:
                # PoDetails.objects.update_or_create(pod_id=pod_id,po=instance, defaults=defaults)
                    PoDetails.objects.filter(pod_id=pod_id,po=instance.po_id).update(**pr_data)
           
            for pr_data in pr_list_data:
                prd = PurchRequistion.objects.filter(pr_id=pr_data.get('pr')).update(pr_status="PO_UNDER_APPROVAL")
            
            # send Notification to restart with lvl 1  approval user 
            self.create_notification(instance, instance.po_approval_lvl_1_users, instance.po_approval_level)
            self.update_notifications_to_read("PR_Return",requestuser.id, instance.pr_id)

        return instance
    
class PoSerializer(serializers.ModelSerializer):
    PR_list = PoDetailSerializer(many=True,write_only=True)   
    PO_delete_list=serializers.ListField(required=False)
    flag=serializers.CharField(write_only=True)
    class Meta:
        model = PoMaster  
        fields ='__all__' 
        extra_kwargs = {
            "status": {"required": False},
            "po_no": {"required": False},
            "created_date": {"required": False},
            "flag": {"required": True}
        }
    def validate_PR_list(self, value):
        if not value:
            raise serializers.ValidationError("PR_list cannot be empty.")
        return value
    def get_pr_list(self, instance):
        pr_list = PoDetails.objects.filter(po=instance.po_id).values(
            'pod_id',
            'po',
            'pr',
            'part',
            'rm',
            'type',
            'req_qty',
            'pr_req_qty',
            'vendor',
            'status',
            rm_mat_name=F('rm__rm_mat_name'),                  
            rm_mat_code=F('rm__rm_mat_code'),                  
            rm_mat_desc=F('rm__rm_mat_desc'),                   
            rm_sec_type=F('rm__rm_sec_type'),                   
            rm_size=F('rm__rm_size'),                   
            rm_hsn_code=F('rm__hsn_code'),                   
            rm_cost=F('rm__rm_cost'),                   
            rm_uom=F('rm__uom'),                     
            rm_image=F('rm__rm_image'),                   
            rm_drawing_no=F('rm__drawing_no'),              
            
            pr_no=F('pr__pr_no'),
            pr_type=F('pr__type'),
            pr_date=F('pr__pr_date'),
            pr_dept_name=F('pr__dept__dept_name'),
            pr_status=F('pr__pr_status'),
            pr_req_by_date=F('pr__req_by_date'),
            pr_approval_level=F('pr__pr_approval_level'),
            pr_approval_lvl_1_users=F('pr__pr_approval_lvl_1_users'),
            pr_approval_lvl_2_users=F('pr__pr_approval_lvl_2_users'),
            pr_lvl_1_appproved=F('pr__pr_lvl_1_approved'),
            pr_lvl_2_appproved=F('pr__pr_lvl_2_approved'),
            pr_remarks=F('pr__remarks'),
            vendor_name=F('vendor__vendor_name'),
            vendor_email=F('vendor__vendor_email'),
            vendor_mobile=F('vendor__vendor_mobile'),
            vendor_city=F('vendor__vendor_city'),
            product_part_no=F('part__product_part_no'),
            product_part_name=F('part__product_part_name'),
            product_part_type=F('part__product_type'),
            product_cost=F('part__product_cost'),
            productt_pic_url=F('part__product_pic_url'),
            product_product_descp=F('part__product_descp'),
        )

        # Create a dictionary to hold the list of vendors for each part_id
        part_vendor_dict = {}
        rm_vendor_dict = {}
        # print(pr_list)
        
        for pr_data in pr_list:
            part_id = pr_data['part']
            part_vendors = PartsVendorsMaster.objects.filter(part=part_id)
           
            part_vendor_list = [{'vendor': vendor.vendor.vendor_id,
                                 'vendor_name':vendor.vendor.vendor_name,
                                  'vendor_city':vendor.vendor.vendor_city,
                                       'vendor_mobile':vendor.vendor.vendor_mobile,
                                       'vendor_email':vendor.vendor.vendor_email,
                                       'vendor_address':vendor.vendor.vendor_address}
                                   for vendor in part_vendors]
            part_vendor_dict[part_id] = part_vendor_list
        for pr_data in pr_list:
            rm_id = pr_data['rm']
            rm_vendors = RmVendorMaster.objects.filter(rm=rm_id)
           
            rm_vendors_vendor_list = [{'vendor': vendor.vendor.vendor_id,
                                       'vendor_name':vendor.vendor.vendor_name,
                                       'vendor_city':vendor.vendor.vendor_city,
                                       'vendor_mobile':vendor.vendor.vendor_mobile,
                                       'vendor_email':vendor.vendor.vendor_email,
                                       'vendor_address':vendor.vendor.vendor_address}
                                         for vendor in rm_vendors]
            rm_vendor_dict[rm_id] = rm_vendors_vendor_list

        for pr_data in pr_list:
           
            part_id = pr_data.get('part')
            pr_data['part_vendor_list'] = part_vendor_dict.get(part_id, [])
            
            rm_id = pr_data.get('rm')
            pr_data['rm_vendor_list'] = rm_vendor_dict.get(rm_id, [])
        
        return pr_list
    def to_representation(self, instance:PoMaster):
        data=super().to_representation(instance)
        data['pr_list']=[]
        data['prp_no']=instance.prp.prp_no
        if instance.po_approval_lvl_1_users:
            user= AuthUser.objects.filter(id=instance.po_approval_lvl_1_users)
            if user:
                if user[0].first_name and user[0].last_name:
                    data['po_approval_lvl_1_users_name']=f'{user[0].first_name} {user[0].last_name}'
                   
                elif user[0].first_name :
                    data['po_approval_lvl_1_users_name']=f'{user[0].first_name}'
                elif user[0].last_name :
                    data['po_approval_lvl_1_users_name']=f'{user[0].last_name}'
        if instance.po_approval_lvl_2_users:
            user= AuthUser.objects.filter(id=instance.po_approval_lvl_2_users)
            if user:
                if user[0].first_name and user[0].last_name:
                    data['po_approval_lvl_2_users_name']=f'{user[0].first_name} {user[0].last_name}'
                elif user[0].first_name :
                    data['po_approval_lvl_2_users_name']=f'{user[0].first_name}'
                elif user[0].last_name :
                    data['po_approval_lvl_2_users_name']=f'{user[0].last_name}'
        # print(instance.prp,"********")
        # data['approval_lvl1_name']=instance.prp.prp_no
        if PoDetails.objects.filter(po=instance.po_id).exists():
            data['pr_list'] = self.get_pr_list(instance)
            # data['pr_list']=PoDetails.objects.filter(po=instance.po_id).values(
            #     'pod_id',
            #     'po',
            #     'pr',
            #     'part',
            #     'req_qty',
            #     'pr_req_qty',
            #     'vendor',
            #     'status',
            #     pr_no=F('pr__pr_no'),
            #     pr_date=F('pr__pr_date'),
            #     pr_dept_name=F('pr__dept__dept_name'),
            #     pr_status=F('pr__pr_status'),
            #     pr_req_by_date=F('pr__req_by_date'),
            #     pr_approval_level=F('pr__pr_approval_level'),
            #     pr_approval_lvl_1_users=F('pr__pr_approval_lvl_1_users'),
            #     pr_approval_lvl_2_users=F('pr__pr_approval_lvl_2_users'),
            #     pr_lvl_1_appproved=F('pr__pr_lvl_1_approved'),
            #     pr_lvl_2_appproved=F('pr__pr_lvl_2_approved'),
            #     pr_remarks=F('pr__remarks'),
            #     vendor_name=F('vendor__vendor_name'),
            #     vendor_email=F('vendor__vendor_email'),
            #     vendor_mobile=F('vendor__vendor_mobile'),
            #     vendor_city=F('vendor__vendor_city'),
            #     product_part_no=F('part__product_part_no'),
            #     product_part_name=F('part__product_part_name'),
            #     product_part_type=F('part__product_type'),
            #     product_cost=F('part__product_cost'),
            #     productt_pic_url=F('part__product_pic_url'),
            #     product_product_descp=F('part__product_descp'),
            # )
        return data
    
    def generate_po_no(self):
        # Extract PO number generation into its own method
        initial_offset = 1
        total_po_count = PoMaster.objects.count()
        new_po_id = total_po_count + initial_offset
        return 'PO{:04d}'.format(new_po_id)

    def handle_pr_list(self, instance, pr_list_data, status):
        # Generalized method to handle PR list creation
        for pr_data in pr_list_data:
            # pr_data.pop('status', None)
            if pr_data.get('pr').type=='PART':
                prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), part=pr_data.get('part'))
            elif pr_data.get('pr').type=='RM':
                prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), rm=pr_data.get('rm'))
    #             # Set a default value if prd does not exist
            
            # prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), rm=pr_data.get('rm'))
            
            pr_data['pr_req_qty'] = prd[0].part_qty if prd.exists() else 0  # Assuming 0 is an acceptable default value
        
            PoDetails.objects.create(po=instance, **pr_data)

    def create_notification(self, instance, user_id, approval_level):
        # Generalized method to create a notification
        message = f"A purchase order with the code {instance.po_no} has been generated. Please click here to approve the PO."
        Notification.objects.create(
            type='PO_Approval',
            message=message,
            created_date=timezone.now(),
            sender_user_id=user_id,
            receiver_user=AuthUser.objects.get(pk=user_id),
            action=instance.po_id,
            is_read=False
        )

    def create(self, validated_data):
        with transaction.atomic():
            request_user=self.context.get('request').user
            flag = validated_data.pop('flag', None)
            pr_list_data = validated_data.pop('PR_list', [])
            po_approval_level = validated_data.get('po_approval_level', None)
            validated_data['po_create_by']=request_user.id

            # Common logic for PO creation
            validated_data['po_no'] = self.generate_po_no()
            validated_data['created_date'] = timezone.now()
            validated_data['status'] = "PO_DRAFT" if flag == "DRAFT" else "PO_UNDER_APPROVAL"
            if flag=="SAVE":
                # print(validated_data.get('po_approval_level'),validated_data.get('po_approval_level')==1)
                if validated_data.get('po_approval_level')==1 and  validated_data.get('po_approval_lvl_1_users') is None:
                    raise serializers.ValidationError({"po_approval_lvl_1_users":['PO approval lvl 1 user field is a required']})
                if validated_data.get('po_approval_level')==2:
                    if  validated_data.get('po_approval_lvl_1_users') is  None:
                        raise serializers.ValidationError({"po_approval_lvl_1_user":['PO approval lvl 1 user field is a required']})
                    if  validated_data.get('po_approval_lvl_2_users') is  None:
                        raise serializers.ValidationError({"po_approval_lvl_2_user":['PO approval lvl 2 user field is a required']})
            instance = super().create(validated_data)

            # Handle PR list based on the flag
            status = "DRAFT" if flag == "DRAFT" else "SAVE"

            
            self.handle_pr_list(instance, pr_list_data, status)
            # print()
            prp_id = validated_data.get('prp')
            PrProcessMaster.objects.filter(prp_id=prp_id.prp_id).update(status="PO_PROCESS")
            # Notification logic for different approval levels
            if flag=="SAVE" and po_approval_level in [1, 2]:
                for pr_data in pr_list_data:
                    # print(pr_data.get('pr'))
                    # prd = PurchRequistion.objects.filter(pr_id=pr_data.get('pr')).update(pr_status="PO_UNDER_APPROVAL")
                    PurchRequistion.objects.filter(pr_id=pr_data.get('pr').pr_id).update(pr_status="PO_UNDER_APPROVAL")
    
                self.create_notification(instance,validated_data.get('po_approval_lvl_1_users') , po_approval_level)
            return instance
    # def create(self, validated_data):
    #     request_user = self.context['request'].user
    #     po_approval_level = validated_data.get('pr_approval_level', None)
    #     flag=validated_data.pop('flag',None)
    #     if flag=="DRAFT":
            
    #         initial_offset = 1  # Start from 1 if there are no records
    #         total_po_count = PoMaster.objects.count()
    #         new_po_id = total_po_count + initial_offset
            
    #         formatted_po_id = 'PO{:04d}'.format(new_po_id)
            
    #         validated_data['po_no'] = formatted_po_id
    #         validated_data['created_date'] = timezone.now()
    #         validated_data['status'] = "PO_DRAFT"

    #         pr_list_data = validated_data.pop('PR_list', [])  # Extract PR_list data
    #         PO_delete_list = validated_data.pop('PO_delete_list', [])  # Extract PR_list data

            
    #         instance = super().create(validated_data)
    #         for pr_data in pr_list_data:
    #             prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), part=pr_data.get('part')).update(pr_status="PO_UNDER_APPROVAL")
    #             # Set a default value if prd does not exist
    #             pr_data['pr_req_qty'] = prd[0].part_qty if prd.exists() else 0  # Assuming 0 is an acceptable default value
    #             pr_data.pop('status',None)
    #             PoDetails.objects.create(po=instance,status="DRAFT" ,**pr_data)
    #     elif flag=="SAVE":
            
    #         initial_offset = 1  # Start from 1 if there are no records
    #         total_po_count = PoMaster.objects.count()
    #         new_po_id = total_po_count + initial_offset
            
    #         formatted_po_id = 'PO{:04d}'.format(new_po_id)
            
    #         validated_data['po_no'] = formatted_po_id
    #         validated_data['created_date'] = timezone.now()
    #         validated_data['status'] = "PO_PENDING"

    #         pr_list_data = validated_data.pop('PR_list', [])  # Extract PR_list data
    #         PO_delete_list = validated_data.pop('PO_delete_list', [])  # Extract PR_list data

    #         instance = super().create(validated_data)

        
    #         for pr_data in pr_list_data:
    #             prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), part=pr_data.get('part')).update(pr_status="PO_UNDER_APPROVAL")
    #             # Set a default value if prd does not exist
    #             pr_data['pr_req_qty'] = prd[0].part_qty if prd.exists() else 0  # Assuming 0 is an acceptable default value
    #             pr_data.pop('status',None)
                
    #             PoDetails.objects.create(po=instance,status="SAVE", **pr_data)

    #         if po_approval_level == 1:
    #                 notification_message = f"A purchase order with the code {formatted_po_id} has been generated. Please click here to approve the PO."  

    #                 notification_user = AuthUser.objects.get(pk=request_user.id)
    #                 notification = Notification.objects.create(
    #                     type='PO_Approval',
    #                     message=notification_message,
    #                     created_date=timezone.now(),
    #                     sender_user_id=request_user.id,
    #                     receiver_user=notification_user,
    #                     action=new_po_id,
    #                     is_read=False
    #                 )

    #         if po_approval_level == 2:
    #                 notification_message = f"A purchase order with the code {formatted_po_id} has been generated. Please click here to approve the PO."  

    #                 notification_user = AuthUser.objects.get(pk=request_user.id)
    #                 notification = Notification.objects.create(
    #                     type='PO_Approval',
    #                     message=notification_message,
    #                     created_date=timezone.now(),
    #                     receiver_user=notification_user,
    #                     sender_user_id=request_user.id,
    #                     action=new_po_id,
    #                     is_read=False
    #                 )
    #     return instance
    

    # def update(self, instance:PoMaster, validated_data):
     
    #     pr_list_data = validated_data.pop('PR_list', [])  
    #     pr_delete_list = validated_data.pop('PO_delete_list', [])  
    #     flag=validated_data.pop('flag',None)
       
    #     instance = super().update(instance, validated_data)
    #     if len(pr_delete_list) > 0:
    #         PoDetails.objects.filter(pod_id__in=pr_delete_list).delete()
    #     # Update or create related PoDetails instances
    #     for pr_data in pr_list_data:

    #         pr_id = pr_data.get('pr', None)
    #         if pr_id is not None:
               
    #             pr_data['pr_req_qty']=prd[0].part_qty
    #             if pr_data.get('pod_id') is not None:
    #                 pr_instance = PoDetails.objects.get(po=instance, pr=pr_id)
    #                 pr_instance.part = pr_data.get('part', pr_instance.part)
    #                 pr_instance.req_qty = pr_data.get('req_qty', pr_instance.req_qty)
    #                 pr_instance.vendor = pr_data.get('vendor', pr_instance.vendor)
    #                 pr_instance.status = pr_data.get('status', pr_instance.status)
    #                 prd=PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'),part=pr_data.get('part'))
    #                 if prd.exists():
    #                     pr_instance.pr_req_qty=prd[0].part_qty
    #                 pr_instance.save()
    #             else:
    #                 prd=PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'),part=pr_data.get('part'))
                     
    #                 if prd.exists():
    #                    pr_data['pr_req_qty']=prd[0].part_qty
    #                 PoDetails.objects.create(po=instance, **pr_data)
    #     if flag=="SAVE" and instance.po_approval_level in [1, 2]:
    #             self.create_notification(validated_data['po_no'], self.context['request'].user.id, instance.po_approval_level)

       
    #     return instance
    @transaction.atomic()
    def update(self, instance: PoMaster, validated_data):
       
            pr_list_data = validated_data.pop('PR_list', [])
            pr_delete_list = validated_data.pop('PO_delete_list', [])
            flag = validated_data.pop('flag', None)
            # print(validated_data)
            validated_data['status'] = "PO_DRAFT" if flag == "DRAFT" else "PO_UNDER_APPROVAL"
            if flag=="SAVE":
                # print(validated_data.get('po_approval_level'),validated_data.get('po_approval_level')==1)
                if validated_data.get('po_approval_level')==1 and  validated_data.get('po_approval_lvl_1_users') is None:
                    raise serializers.ValidationError({"po_approval_lvl_1_users":['PO approval lvl 1 user field is a required']})
                if validated_data.get('po_approval_level')==2:
                    if  validated_data.get('po_approval_lvl_1_users') is  None:
                        raise serializers.ValidationError({"po_approval_lvl_1_user":['PO approval lvl 1 user field is a required']})
                    if  validated_data.get('po_approval_lvl_2_users') is  None:
                        raise serializers.ValidationError({"po_approval_lvl_2_user":['PO approval lvl 2 user field is a required']})
            instance = super().update(instance, validated_data)
            # Efficient deletion
            if pr_delete_list:
                PoDetails.objects.filter(pod_id__in=pr_delete_list).delete()

            # Pre-fetch PurchRequistionDetails
            # pr_ids = [pr_data['pr'] for pr_data in pr_list_data if 'pr' in pr_data]
            # prd_qs = PurchRequistionDetails.objects.filter(pr__in=pr_ids).annotate(pr=F('pr'), part_id=F('part')).values('pr', 'part', 'part_qty')
            # prd_map = {(prd['pr'], prd['part']): prd['part_qty'] for prd in prd_qs}
            # pr_ids = [pr_data['pr'] for pr_data in pr_list_data if 'pr' in pr_data]
            # prd_qs = PurchRequistionDetails.objects.filter(pr__in=pr_ids).annotate(
            #     annotated_pr=F('pr'), annotated_part=F('part')
            # ).values('annotated_pr', 'annotated_part', 'part_qty')
            
            # # Now, adjust the map to use the new annotation names
            # prd_map = {(prd['annotated_pr'], prd['annotated_part']): prd['part_qty'] for prd in prd_qs}

            # Update or create PoDetails instances
            for pr_data in pr_list_data:
                # pr_id, part_id = pr_data.get('pr'), pr_data.get('part')
                # pr_req_qty = prd_map.get((pr_id, part_id), 0)  # Default to 0 if not found
                # pr_data['pr_req_qty'] = pr_req_qty
                prd = PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'), part=pr_data.get('part'))
                   # Set a default value if prd does not exist
                pr_data['pr_req_qty'] = prd[0].part_qty if prd.exists() else 0  # Assuming 0 is an acceptable default value
        
                # Update or create logic
                pod_id = pr_data.pop('pod_id', None)
                defaults = {key: value for key, value in pr_data.items()}
                # print("defauts",defaults,pr_data)  
                PoDetails.objects.update_or_create(pod_id=pod_id,po=instance, defaults=defaults)

            # Send notification if applicable
            if flag == "SAVE" and instance.po_approval_level in [1, 2]:
                for pr_data in pr_list_data:
                    # prd = PurchRequistion.objects.filter(pr_id=pr_data.get('pr').pr_id).update(pr_status="PO_UNDER_APPROVAL")
                    PurchRequistion.objects.filter(pr_id=pr_data.get('pr').pr_id).update(pr_status="PO_UNDER_APPROVAL")
                self.create_notification(instance, validated_data.get('po_approval_lvl_1_users'), instance.po_approval_level)

            return instance
    

    # om code 
  # Include all fields for PoDetails
    


# class PoSerializer(serializers.ModelSerializer):
#     PR_list = PoDetailSerializer(many=True,write_only=True)   
#     PO_delete_list=serializers.ListField(required=False)
#     class Meta:
#         model = PoMaster  
#         fields ='__all__' 
#         extra_kwargs = {
#             "status": {"required": False},
#             "po_no": {"required": False},
#             "created_date": {"required": False}
#         }
#     def validate_PR_list(self, value):

#         if not value:
#             raise serializers.ValidationError("PR_list cannot be empty.")
#         return value
#     def to_representation(self, instance):
#         data=super().to_representation(instance)
#         data['pr_list']=[]
#         data['prp_no']=instance.prp.prp_no
#         if PoDetails.objects.filter(po=instance.po_id).exists():
        
#             data['pr_list']=PoDetails.objects.filter(po=instance.po_id).values(
#                 'pod_id',
#                 'po',
#                 'pr',
#                 'part',
#                 'req_qty',
#                 'pr_req_qty',
#                 'vendor',
#                 'status',
#                 pr_no=F('pr__pr_no'),
#                 pr_date=F('pr__pr_date'),
#                 pr_dept_name=F('pr__dept__dept_name'),
#                 pr_status=F('pr__pr_status'),
#                 pr_req_by_date=F('pr__req_by_date'),
#                 pr_approval_level=F('pr__pr_approval_level'),
#                 pr_approval_lvl_1_users=F('pr__pr_approval_lvl_1_users'),
#                 pr_approval_lvl_2_users=F('pr__pr_approval_lvl_2_users'),
#                 pr_lvl_1_appproved=F('pr__pr_lvl_1_approved'),
#                 pr_lvl_2_appproved=F('pr__pr_lvl_2_approved'),
#                 pr_remarks=F('pr__remarks'),
#                 vendor_name=F('vendor__vendor_name'),
#                 vendor_email=F('vendor__vendor_email'),
#                 vendor_mobile=F('vendor__vendor_mobile'),
#                 vendor_city=F('vendor__vendor_city'),
#                 product_part_no=F('part__product_part_no'),
#                 product_part_name=F('part__product_part_name'),
#                 product_part_type=F('part__product_type'),
#                 product_cost=F('part__product_cost'),
#                 productt_pic_url=F('part__product_pic_url'),
#                 product_product_descp=F('part__product_descp'),
#             )
#         return data
#     def create(self, validated_data):
#         print(validated_data)
#         try:
#             l_po_id = PoMaster.objects.latest('po_no') 
#         except PoMaster.DoesNotExist:
#             l_po_id = None
        
#         new_po_id = 1
#         latest_po_no = l_po_id.po_no if l_po_id else None     
#         if latest_po_no:  
#             # Increment the latest mrs_id by 1
#             current_po_id = int(latest_po_no[2:])
#             new_po_id = current_po_id + 1
         
#         formatted_po_id = 'PO{:04d}'.format(new_po_id)
#         validated_data['po_no'] = formatted_po_id
#         validated_data['created_date'] = timezone.now()
#         validated_data['status'] = "PO_PENDING"

#         pr_list_data = validated_data.pop('PR_list', [])  # Extract PR_list data
#         PO_delete_list = validated_data.pop('PO_delete_list', [])  # Extract PR_list data

#         instance = super().create(validated_data)

#         # Create related PoDetails instances
#         for pr_data in pr_list_data:
#             prd=PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'),part=pr_data.get('part'))
#             if prd.exists():
#                 pr_data['pr_req_qty']=prd[0].part_qty
#             PoDetails.objects.create(po=instance, **pr_data)

#         return instance

#     def update(self, instance, validated_data):
     
#         pr_list_data = validated_data.pop('PR_list', [])  
#         pr_delete_list = validated_data.pop('PO_delete_list', [])  

#         instance = super().update(instance, validated_data)

#         # Update or create related PoDetails instances
#         for pr_data in pr_list_data:

#             pr_id = pr_data.get('pr', None)
#             if pr_id is not None:
               
#                 pr_data['pr_req_qty']=prd[0].part_qty
#                 if pr_data.get('pod_id') is not None:
#                     pr_instance = PoDetails.objects.get(po=instance, pr=pr_id)
#                     pr_instance.part = pr_data.get('part', pr_instance.part)
#                     pr_instance.req_qty = pr_data.get('req_qty', pr_instance.req_qty)
#                     pr_instance.vendor = pr_data.get('vendor', pr_instance.vendor)
#                     pr_instance.status = pr_data.get('status', pr_instance.status)
#                     prd=PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'),part=pr_data.get('part'))
#                     if prd.exists():
#                         pr_instance.pr_req_qty=prd[0].part_qty
#                     pr_instance.save()
#                 else:
#                     prd=PurchRequistionDetails.objects.filter(pr=pr_data.get('pr'),part=pr_data.get('part'))
                     
#                     if prd.exists():
#                        pr_data['pr_req_qty']=prd[0].part_qty
#                     PoDetails.objects.create(po=instance, **pr_data)

#         if len(pr_delete_list) > 0:
#             PoDetails.objects.filter(pod_id__in=pr_delete_list).delete()
#         return instance
