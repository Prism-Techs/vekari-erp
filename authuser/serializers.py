from collections import defaultdict
import os
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import APIException,ValidationError
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from .backends import AuthenticateJWT
from django.contrib.auth.hashers import check_password
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.encoding import  smart_str ,force_bytes,force_str
from .utils import Util
from django.core.files.storage import FileSystemStorage 
from datetime import datetime ,date
from vekaria_erp.settings import PRODUCTION,HOST_URL,LOCALHOST
from django.utils import timezone

class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        auth= AuthUser.objects.get(id=user.id)
        token['username'] = user.username
        token['email'] = user.email
        token['staff'] = user.is_staff
        AuthUser.objects.filter(id=user.id).update(last_login=timezone.now())
        
         
        return token
    def validate(self, attrs):
        credentials = {
            'username': attrs.get('username'),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = AuthenticateJWT().authenticate(
                self.context['request'],
                username=credentials['username'],
                password=credentials['password']
            )
            if user:
                refresh = self.get_token(user)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                client_ip = self.context['request'].META.get('REMOTE_ADDR')
                
                AuthUser.objects.filter(id=user.id).update(last_ip_address=client_ip)

                return data
            else:
                if AuthUser.objects.filter(username=credentials['username']).exists():
                    msg="Password is incorrect, please try again or you can click on forget Password."
                else:
                    msg="This username is not registered, please sign up."

               
                raise serializers.ValidationError({"error":msg})

        else:
            msg = '"username" and "password" are required.'
            raise serializers.ValidationError({"error":msg})
    

class UserSerializer(serializers.ModelSerializer):
    group = serializers.ListField(child=serializers.CharField(), required=False)
    class Meta:
        model=AuthUser     
        # field=[]
        exclude=['is_superuser'] 
        extra_kwargs = {
            "first_name": {"allow_null": True},
            "last_name": {"allow_null": True},
            "date_joined": {"required": False},
            "is_admin": {"required": False},
            "is_staff": {"required": False},
            "is_active": {"required": False},
            "password": {"required": False},
            "is_superuser": {"required":False}

        }


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        permission_mapping = {
            1: "create",
            2: "update",
            3: "delete",
            4: "view"
        }
        group = {}

        # Fetch the user object using the user ID
        user_id = representation.get('id')
        if user_id is not None:
            try:
                user = AuthUser.objects.get(pk=user_id)
            except AuthUser.DoesNotExist:
                user = None

        if user:
            old_usergroup_obj = UserPermission.objects.filter(user=user_id).values('group', 'permission')
            all_group_obj = UserPermissionGroup.objects.all()
            all_group_list = [group.id for group in all_group_obj]
# # Create a dictionary to store group-permission associations
            group_permission_dict = defaultdict(list)
            for entry in old_usergroup_obj:
                    group_id = entry['group']
                    permission_id = entry['permission']
                    if group_id in all_group_list and permission_id not in group_permission_dict[group_id]:
                        group_permission_dict[group_id].append(permission_id)

            representation['group'] = [{str(group_id): permission_ids for group_id, permission_ids in group_permission_dict.items()}]


            # group_name and true and false 
            group_list = UserPermission.objects.filter(user=user).values('group__group_name', 'group')
            for group_list_value in group_list:
                if group_list_value['group__group_name'] not in group:
                    group_permission = UserPermission.objects.filter(user=user, group=group_list_value['group']).values('permission')
                    group[group_list_value['group__group_name']] = {
                        "create": False,
                        "update": False,
                        "delete": False,
                        "view": False
                    }
                    for permission in group_permission:
                        permission_type = permission_mapping.get(permission['permission'])
                        if permission_type:
                            group[group_list_value['group__group_name']][permission_type] = True

        representation['group_name'] = [group]  

        representation.pop('password', None)
        return representation
    # def validate_email(self, value):
    #     user = self.instance  # Get the current user instance being updated
    #     if user is not None and user.email == value:
    #         return value  # Email not changed, no need to perform validation

    #     if User.objects.filter(email=value).exists():
    #         raise serializers.ValidationError("This email address is already in use.")
    #     return value
    def update(self, instance, validated_data):
        requestuser = self.context['request'].user

        instance.update_profile_by=requestuser.id

        return super().update(instance, validated_data)

    def create(self, validated_data):
        email= validated_data.get('email')
        username= validated_data.get('username')
        password= validated_data.get('password')
        mobile_no= validated_data.get('mobile_no')
        requestuser = self.context['request'].user
        print(validated_data,mobile_no,requestuser)
        if username=='' or username is  None:
            raise serializers.ValidationError({"error": "username is required"})
        if password=='' or password is  None:
            raise serializers.ValidationError({"error": "password is required"})
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({"error":"Username is already existed."})
        # if email!='' or email is not None or email !="null":
        #     if User.objects.filter(email=email).exists():
        #         raise serializers.ValidationError({"error":"Email is already existed."})
        if mobile_no is not None and mobile_no != '' and mobile_no != "null":   
            if len(str(mobile_no))!=10:
                raise serializers.ValidationError({"error":"Only allow 10 digit number."})
            if AuthUser.objects.filter(mobile_no=mobile_no).exists():
                raise serializers.ValidationError({"error":"mobile_no is already existed."})
        user = User.objects.create(email=email,username=username,first_name=validated_data.get('first_name'),last_name=validated_data.get('last_name'))
        print(user.id)
        Auth=AuthUser.objects.filter(id=user.id).update(creation_by=requestuser.id,mobile_no=mobile_no)
        user.set_password(password)
        user.save()

        return user


class ProfileSerializer(serializers.ModelSerializer):
    profile_upload=serializers.FileField(allow_null=True,required=False,)
    del_userimage = serializers.BooleanField(default=False,required=False)

    def validate(self, attrs):
        if attrs.get('mobile_no') is not  None or attrs.get('mobile_no') =="": 
            if len(str(attrs.get('mobile_no','')))!=10:
                    raise serializers.ValidationError({"error":"Only allow 10 digit number."})
    
        return attrs
    class Meta:
        model=AuthUser
        fields=['username','email','first_name','last_name','profile_upload','profile_url','mobile_no','del_userimage']
        exclude=[]
        extra_kwargs = {
            "first_name":{
                "allow_null":True
            },
            "last_name":{
                "allow_null":True
            },    
            "profile_url":{
                "required":False
            },
            "mobile_no":{
                "required":False
            },
            
        }
    def update(self, instance, validated_data):
        print(validated_data)
        del_userimage = validated_data.get('del_userimage', False)
        profile_upload = validated_data.get('profile_upload', None)

        if del_userimage:
        
            cp = os.getcwd()
            p = str(cp + instance.profile_url)
            p = p.replace('\\', '/')
            p = p.replace('%20', ' ')
            p = p.replace('%40', '@')
            # print("photo", p)
            try:
                os.remove(p)
            except Exception as e:
                print("delete profile img error :",e)
            instance.profile_url = None
            instance.save()
        if profile_upload != None:
            if len(profile_upload) != 0:
                print("in")
                if instance.profile_url != None:
                    cp = os.getcwd()
                    p = str(cp + instance.profile_url)
                    p = p.replace('\\', '/')
                    p = p.replace('%20', ' ')
                    p = p.replace('%40', '@')
                    print(p)
                    try:
                        os.remove(p)
                    except Exception as e:
                        print("delete profile img error :",e)
                fs=FileSystemStorage()
                profile_name= profile_upload.name
                profile_name= profile_name.replace(' ', '_')
                filename = fs.save('profile/' +str(instance.id)+"/" + profile_name,
                                   profile_upload)
                profile_url = fs.url(filename)
            
                instance.profile_url = profile_url
                instance.save()
            else:
                instance.profile_url = None
            instance.update_profile_by=instance.id
            instance.save()
        
        return super().update(instance, validated_data)
class UserChangePasswordSerializer(serializers.Serializer):
    currentpassword=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    newpassword=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['currentpassword','newpassword']
    def validate(self, attrs):
            currentpassword= attrs.get('currentpassword')
            newpassword=attrs.get('newpassword') 
            user=self.context.get('user')
            usercurrentpassword= user.password
            match_password=check_password(currentpassword,usercurrentpassword)
           
            if not match_password:
                raise serializers.ValidationError("Current Password is incorrect")
            
            
            user.set_password(newpassword)
            user.save()
            return attrs
    



class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    class Meta:
        fields=['email']
    def validate(self,attrs):
            email= attrs.get('email','')
            print("email",email)
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uid= urlsafe_base64_encode(force_bytes(user.id))
                print('Encode id:',uid)
                token=PasswordResetTokenGenerator().make_token(user)
                print("reset password Token:= ",token)
                link='http://localhost:4200/#/auth/reset-password/'+uid+'/'+token+'/'
                print('reset password link :=',link)
                body='Click Following Link to Reset Your Password:'+link 
                data={
                    'subject':'Reset Your Password',
                    'body':body,
                    'link':link,
                    'username':user.username,
                    'to_email':user.email
                }
                Util.send_reset_password_email(data)
                return attrs
            else:
                raise serializers.ValidationError({"error":'This email is not registered, please sign up.'})
            
class UserPasswordResetViewSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        try:
            user_id = user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"error":'Invalid reset password link'})

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"error":'Invalid reset password link'})

        attrs['user'] = user
        attrs['new_password'] = new_password
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermission
        fields = '__all__'

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalMaster
        exclude=[]

        
class UserApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApproval
        exclude=[]
        extra_kwargs = {
            "user":{
                "required":False
            }}
    def to_representation(self, instance:UserApproval):
        data= super().to_representation(instance)
        data['approval_name']=instance.approval.approval_name
    
        return data
      
class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=2)
    class Meta:
        fields=['email']
    def validate(self,attrs):
            email= attrs.get('email','')
            print("email",email)
            if User.objects.filter(email=email).exists():
                user = User.objects.get(email=email)
                uid= urlsafe_base64_encode(force_bytes(user.id))
                print('Encode id:',uid)
                token=PasswordResetTokenGenerator().make_token(user)
                print("reset password Token:= ",token)
                if PRODUCTION:
                    link=f'{HOST_URL}/auth/reset-password/'+uid+'/'+token+'/'
                else:
                    link=f'{LOCALHOST}/auth/reset-password/'+uid+'/'+token+'/'
                print('reset password link :=',link)
                body='Click Following Link to Reset Your Password:'+link 
                data={
                    'subject':'Reset Your Password',
                    'body':body,
                    'link':link,
                    'username':user.username,
                    'to_email':user.email
                }
                try:
                    Util.send_reset_password_email(data)
                except Exception as e:

                    print('Error =>',e)
                    raise serializers.ValidationError({"error":"Send email failed"})
                return attrs
            else:
                raise serializers.ValidationError({"error":'This email is not registered, please sign up.'})

class UserPasswordResetViewSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')
        new_password = attrs.get('new_password')

        try:
            user_id = user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({"error":'Invalid reset password link'})
    
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError({"error":'Invalid reset password link'})

        attrs['user'] = user
        attrs['new_password'] = new_password
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()