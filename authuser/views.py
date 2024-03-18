from django.http import Http404
from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.models import User
from django.db.models import Q
from .permission import YourPermission, group_permissions
from collections import defaultdict
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters  

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class UserView(
    generics.ListCreateAPIView,
    generics.RetrieveUpdateDestroyAPIView,):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = AuthUser.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    group_permissions = ["settings"]

    def perform_create(self, serializer):
        # Associate the authenticated user with the new object
        serializer.save(user=self.request.user)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        if pk is not None:
            if User.objects.filter(id=pk).exists():
                user = AuthUser.objects.get(id=pk)
                serializer = UserSerializer(user)

                context = serializer.data

                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Not Fonud in Record"}, status=status.HTTP_404_NOT_FOUND
                )

        else:
            search = request.query_params.get("search")
            paginator = StandardResultsSetPagination()
            user = (
                AuthUser.objects.all()
                .order_by("-date_joined")
                .exclude(is_superuser=True)
            )
            is_active = request.query_params.get("is_active")
            if is_active is not None:
                user = user.filter(Q(is_active=is_active)).exclude(is_superuser=True)

            if search is not None:
                user = user.filter(
                    Q(username__icontains=search)
                    | Q(email__icontains=search)
                    | Q(first_name__icontains=search)
                    | Q(last_name__icontains=search)
                ).exclude(is_superuser=True)
            result_page = paginator.paginate_queryset(user, request)
            serializer = UserSerializer(result_page, many=True)
            context = serializer.data
            return paginator.get_paginated_response(context)


class ProfileView(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        return AuthUser.objects.get(id=self.request.user.id)


class UserChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, format=None):
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Change Password Successfully "}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordEmailRequest(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response(
                {"message": "Password reset link sent.Please check your email "},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPasswordResetView(APIView):
    def post(self, request, uid, token):
        serializer = UserPasswordResetViewSerializer(
            data={
                "uid": uid,
                "token": token,
                "new_password": request.data.get("new_password"),
            }
        )
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({"message": "Password reset successfully"})


class PermissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        if pk is not None:
            if AuthUser.objects.filter(id=pk).exists():
                user = AuthUser.objects.get(id=pk)
                permission_data = {}
                permission_data["admin"] = user.is_admin
                permission_data["super_admin"] = user.is_superuser
                all_group = UserPermissionGroup.objects.all().values("group_name", "id")
                viewcode = Permission.objects.get(permission_name="view")
                createcode = Permission.objects.get(permission_name="create")
                updatecode = Permission.objects.get(permission_name="update")
                deletecode = Permission.objects.get(permission_name="delete")

                for group in all_group:
                    group_name = group["group_name"]
                    group_id = group["id"]
                    Permission_group = "permission_" + group_name
                    permissions = UserPermission.objects.filter(
                        user=user.id,
                        group__group_name=group_name,
                        permission__permission_name__in=[
                            "create",
                            "update",
                            "delete",
                            "view",
                        ],
                    )
                    permission_data[Permission_group] = permissions.exists()
                    permission_data["create_code"] = createcode.id
                    permission_data["update_code"] = updatecode.id
                    permission_data["delete_code"] = deletecode.id
                    permission_data["view_code"] = viewcode.id
                    # print(group_name,view_permission)
                    # permission_data[Permission_group]=UserPermission.objects.filter(user=user.id,group__group_name=group_name,permission__permission_name__in=['create','update','delete','view']).exists()
                    permission_data[group_name] = {
                        "id": group_id,
                        "view": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="view",
                        ).exists(),
                        "create": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="create",
                        ).exists(),
                        "delete": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="delete",
                        ).exists(),
                        "update": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="update",
                        ).exists(),
                    }
                    all_group_obj = UserPermissionGroup.objects.all()
                    all_group_list = [group.id for group in all_group_obj]
                    old_usergroup_obj = UserPermission.objects.filter(user=pk).values(
                        "group", "permission"
                    )

                    # Create a dictionary to store group-permission associations
                    group_permission_dict = defaultdict(list)

                    for entry in old_usergroup_obj:
                        group_id = entry["group"]
                        permission_id = entry["permission"]
                        if (
                            group_id in all_group_list
                            and permission_id not in group_permission_dict[group_id]
                        ):
                            group_permission_dict[group_id].append(permission_id)

                    permission_data["group"] = {
                        str(group_id): permission_ids
                        for group_id, permission_ids in group_permission_dict.items()
                    }

                return Response(permission_data)
        else:
            raise ValidationError({"message": "Parameter userid is required in URL."})

    def put(self, request, pk=None):
        if pk is not None:
            try:
                if AuthUser.objects.filter(id=pk).exists():
                    auth = AuthUser.objects.get(id=pk)
                    if request.data.get("group"):
                        all_group_obj = UserPermissionGroup.objects.all()
                        all_group_list = [group.id for group in all_group_obj]

                        new_usergroup_dict = request.data.get("group")
                        old_usergroup_obj = UserPermission.objects.filter(user=pk).values(
                            "group", "permission"
                        )

                        # Create a dictionary to store group-permission associations
                        group_permission_dict = defaultdict(list)

                        for entry in old_usergroup_obj:
                            group_id = entry["group"]
                            permission_id = entry["permission"]
                            if (
                                group_id in all_group_list
                                and permission_id not in group_permission_dict[group_id]
                            ):
                                group_permission_dict[group_id].append(permission_id)

                        old_usergroup_dict = {
                            str(group_id): permission_ids
                            for group_id, permission_ids in group_permission_dict.items()
                        }

                        print("old", old_usergroup_dict)
                        print("new", new_usergroup_dict)

                        # Update permissions lists for overlapping groups in unique_union_dict
                        unique_union_dict = {
                            group_id: list(
                                set(permission_ids + new_usergroup_dict.get(group_id, []))
                            )
                            for group_id, permission_ids in old_usergroup_dict.items()
                        }

                        # Add new groups from new_usergroup_dict
                        for group_id, permission_ids in new_usergroup_dict.items():
                            if group_id not in old_usergroup_dict:
                                unique_union_dict[group_id] = permission_ids

                        print("unique_union_dict", unique_union_dict)

                        # Calculate the dictionary of items to be deleted

                        # del_dict = {
                        #     group_id: [permission_id for permission_id in permission_ids if permission_id not in new_usergroup_dict.get(group_id, [])]
                        #     for group_id, permission_ids in unique_union_dict.items()
                        # }

                        del_dict = {
                            group_id: [
                                permission_id
                                for permission_id in permission_ids
                                if permission_id not in new_usergroup_dict.get(group_id, [])
                            ]
                            for group_id, permission_ids in unique_union_dict.items()
                            if [
                                permission_id
                                for permission_id in permission_ids
                                if permission_id not in new_usergroup_dict.get(group_id, [])
                            ]
                        }

                        print("del_dict", del_dict)
                        for group_id, permission_ids in del_dict.items():
                            del_userpermission = UserPermission.objects.filter(
                                user=pk, group=group_id, permission__in=permission_ids
                            ).delete()
                            print(del_userpermission)
                    
                        for group_id, permission_ids in new_usergroup_dict.items():
                            for pid in permission_ids:
                                if not UserPermission.objects.filter(
                                    user=pk, group=group_id, permission=pid
                                ).exists():
                                    print("create: ", group_id, ": ", pid)
                                    group_obj = UserPermissionGroup.objects.get(id=group_id)
                                    permission_obj = Permission.objects.get(id=pid)
                                    UserPermission.objects.create(
                                        user=auth,
                                        group=group_obj,
                                        permission=permission_obj,
                                    )

                  
                    return Response({"message": "permission sucessfully updated."})
                else:
                    return Response({"message": "Not Found User."})

            except Exception as e:
                print(e)
                raise ValidationError(
                    {"message": "internal server errror", "error": str(e)}
                )

        else:
            raise ValidationError({"message": "Parameter userid is required in URL."})


class AllpermissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        all_group = UserPermissionGroup.objects.all().values("group_name", "id")
        all_permission = Permission.objects.all().values("permission_name", "id")
        per = [
            {all_per["permission_name"]: all_per["id"] for all_per in all_permission}
        ]
        # print(per)
        data = {"group": all_group, "permission": per[0]}
        return Response([data])


class NavPermissionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pk = request.user.id
        if pk is not None:
            if AuthUser.objects.filter(id=pk).exists():
                user = AuthUser.objects.get(id=pk)
                permission_data = {}
                permission_data["admin"] = user.is_admin
                permission_data["super_admin"] = user.is_superuser
                all_group = UserPermissionGroup.objects.all().values("group_name", "id")
                viewcode = Permission.objects.get(permission_name="view")
                createcode = Permission.objects.get(permission_name="create")
                updatecode = Permission.objects.get(permission_name="update")
                deletecode = Permission.objects.get(permission_name="delete")

                for group in all_group:
                    group_name = group["group_name"]
                    group_id = group["id"]
                    Permission_group = "permission_" + group_name
                    permissions = UserPermission.objects.filter(
                        user=user.id,
                        group__group_name=group_name,
                        permission__permission_name__in=[
                            "create",
                            "update",
                            "delete",
                            "view",
                        ],
                    )
                    permission_data[Permission_group] = permissions.exists()
                    permission_data["create_code"] = createcode.id
                    permission_data["update_code"] = updatecode.id
                    permission_data["delete_code"] = deletecode.id
                    permission_data["view_code"] = viewcode.id
                    # print(group_name,view_permission)
                    # permission_data[Permission_group]=UserPermission.objects.filter(user=user.id,group__group_name=group_name,permission__permission_name__in=['create','update','delete','view']).exists()
                    permission_data[group_name] = {
                        "id": group_id,
                        "view": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="view",
                        ).exists(),
                        "create": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="create",
                        ).exists(),
                        "delete": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="delete",
                        ).exists(),
                        "update": UserPermission.objects.filter(
                            user=user.id,
                            group__group_name=group_name,
                            permission__permission_name="update",
                        ).exists(),
                    }
                    all_group_obj = UserPermissionGroup.objects.all()
                    all_group_list = [group.id for group in all_group_obj]
                    old_usergroup_obj = UserPermission.objects.filter(user=pk).values(
                        "group", "permission"
                    )

                    # Create a dictionary to store group-permission associations
                    group_permission_dict = defaultdict(list)

                    for entry in old_usergroup_obj:
                        group_id = entry["group"]
                        permission_id = entry["permission"]
                        if (
                            group_id in all_group_list
                            and permission_id not in group_permission_dict[group_id]
                        ):
                            group_permission_dict[group_id].append(permission_id)

                    permission_data["group"] = {
                        str(group_id): permission_ids
                        for group_id, permission_ids in group_permission_dict.items()
                    }

                return Response(permission_data)
        else:
            raise ValidationError(
                {"message": "You are Unauthorized, Please Login System.."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        
        
class ApprovalAPIView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = ApprovalMaster.objects.all()
    serializer_class = ApprovalSerializer
    group_permissions = ['settings']
    # pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['approval_name', ]
    # Specify the fields by which the client can order the results
    ordering_fields = ['approval_name']
    # Default ordering
    ordering = ['-approval_id']

class ApprovalRetrieveAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = ApprovalMaster.objects.all()
    serializer_class = ApprovalSerializer
    group_permissions = ['settings']


class UserApprovalRetrieveAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
   
    group_permissions = ['settings']
    def get(self, request, *args, **kwargs):
        user = kwargs.get('userid')
        
        if user is not None:
            if AuthUser.objects.filter(id=user).exists():
                instance = UserApproval.objects.filter(user=user)
                serializer = UserApprovalSerializer(instance=instance, many=True)
                # You probably want to return the serialized data here
                return Response(serializer.data)
            else:
                return Response({"error": "User Not Found."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User id querystring is required."}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        user=kwargs.get('userid')
        approval_list= request.data.get('approval_list',[])
        if approval_list is None or len(approval_list) ==0 :
            return Response({"message":"approval_list is a required"}) 
        if user is not None:
            if AuthUser.objects.filter(id=user).exists():
                serializer_list=[]
                serializer_error_list=[]
                
                for approv in approval_list:
                    approv['user']=user   
                    if UserApproval.objects.filter(user=user,approval=approv.get('approval')).exists():

                            instance=  UserApproval.objects.filter(user=user,approval=approv.get('approval')).first()
                          
                            approv['modify_by']=request.user.id
                            approv['modify_date']=timezone.now()
                            serializer= UserApprovalSerializer(instance=instance,data=approv)
                            if serializer.is_valid():
                                serializer_list.append(serializer)
                            else:
                                
                                serializer_error_list.append(serializer.errors)


                            print("=======update======",approv)

                    else:   
                            print("=======create======",approv)
                            approv['create_by']=request.user.id
                            approv['create_date']=timezone.now()
                            serializer= UserApprovalSerializer(data=approv)
                            # print(serializer.is_valid(),serializer.errors)
                            if serializer.is_valid():
                                serializer_list.append(serializer)
                            else:
                                
                                print(serializer.errors)
                            
                                serializer_error_list.append(serializer.errors)

                if len(serializer_error_list)!=0:
                    print("serializer_error_list=====",serializer_error_list) 
                    return Response({"error":serializer_error_list},status=status.HTTP_400_BAD_REQUEST)
                else:
                    for user_serial in serializer_list:
                        user_serial.save()
                return Response({"message":"User sucessfully permission set"})
            return Response({"error":"User Not Found."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message":"User id querystring is required."},status=status.HTTP_400_BAD_REQUEST)



class UserApprovalAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserApprovalSerializer
   
    def get_queryset(self):
        return UserApproval.objects.filter(user=self.request.user.id)
    
class ResetPasswordEmailRequest(APIView):
    authentication_classes = []
    serializer_class=ResetPasswordEmailRequestSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer=self.serializer_class(data=request.data)
        try:
            if serializer.is_valid(raise_exception=True):
                return Response({'message':'Password reset link sent.Please check your email '},status=status.HTTP_200_OK)
        except:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
class UserPasswordResetView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    

    def post(self, request, uid, token):
        serializer = UserPasswordResetViewSerializer(data={'uid': uid, 'token': token, 'new_password': request.data.get('new_password')})
        serializer.is_valid(raise_exception=True)
        
        serializer.save()

        return Response({'message': 'Password reset successfully'})
    
# jay code 
class ActiveUsersView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, YourPermission]
    queryset = AuthUser.objects.all().order_by('date_joined').filter(is_active=True)
    serializer_class = UserSerializer
    
# users data entry 
# class userlist(APIView):
#     def get(self, request, *args, **kwargs):
#         udata = [
#             {
#                 "username": "adminV",
#                 "password": "admin@123",
#                 "first_name": "Ravi",
#                 "last_name": "Vaghela",
#                 "email": "ravivaghela.net@gmail.com",
#                 "mobile_no": "8320309790",
#             },
#             {
#                 "username": "manoj",
#                 "password": "564495",
#                 "first_name": "Manoj",
#                 "last_name": "Chandra",
#                 "email": "it@vekaria.com",
#                 "mobile_no": "9898194699",
#             },
#             {
#                 "username": "pillai",
#                 "password": "ns#1011",
#                 "first_name": "Shiva Shankar",
#                 "last_name": "Pillai",
#                 "email": "info@vekaria.com",
#                 "mobile_no": "9909908037",
#             },
#             {
#                 "username": "ratnesh",
#                 "password": "PROD#1106",
#                 "first_name": "Ratnesh",
#                 "last_name": "Jadvani",
#                 "email": "production@vekaria.com",
#                 "mobile_no": "9909909475",
#             },
#             {
#                 "username": "reception",
#                 "password": "vekaria",
#                 "first_name": "Chetan",
#                 "last_name": "Bhoot",
#                 "email": "frontdesk@vekaria.com",
#                 "mobile_no": "02882551093",
#             },
#             {
#                 "username": "chetan",
#                 "password": "vekaria",
#                 "first_name": "Chetan",
#                 "last_name": "Bhoot",
#                 "email": "frontdesk@vekaria.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "satish",
#                 "password": "vekaria",
#                 "first_name": "Satish",
#                 "last_name": "Talsaniya",
#                 "email": "training-solutions@vekaria.com",
#                 "mobile_no": "7096474746",
#             },
#             {
#                 "username": "vaibhav",
#                 "password": "qa#1411",
#                 "first_name": "Vaibhav",
#                 "last_name": "Vithalani",
#                 "email": "qc.vekaria@gmail.com",
#                 "mobile_no": "9374883236",
#             },
#             {
#                 "username": "sumit",
#                 "password": "qc#1301",
#                 "first_name": "Sumit",
#                 "last_name": "Tejani",
#                 "email": "qc.vekaria@gmail.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "divyesh",
#                 "password": "dv#0906",
#                 "first_name": "Divyesh",
#                 "last_name": "Vadgama",
#                 "email": "store.vekaria@gmail.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "jayesh",
#                 "password": "str#2712",
#                 "first_name": "Jayesh",
#                 "last_name": "Peshavariya",
#                 "email": "store.vekaria@gmail.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "devang",
#                 "password": "vekaria",
#                 "first_name": "Devang",
#                 "last_name": "Thakkar",
#                 "email": "frontdesk@vekaria.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "SS",
#                 "password": "SS#1009",
#                 "first_name": "Sanjiv",
#                 "last_name": "Sabarwal",
#                 "email": "sales@vekaria.com",
#                 "mobile_no": "9909921851",
#             },
#             {
#                 "username": "kapdi",
#                 "password": "vekaria",
#                 "first_name": "Dalpatram",
#                 "last_name": "Kapdi",
#                 "email": "purchase@vekaria.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "bsv",
#                 "password": "vekaria",
#                 "first_name": "Bhupendra",
#                 "last_name": "Vekaria",
#                 "email": "bsvekaria@vekaria.com",
#                 "mobile_no": "9824245693",
#             },
#             {
#                 "username": "Dipesh",
#                 "password": "dv#1206",
#                 "first_name": "Dipesh",
#                 "last_name": "Vora",
#                 "email": "hr@vekaria.com",
#                 "mobile_no": "9909921069",
#             },
#             {
#                 "username": "SANJIV",
#                 "password": "1963",
#                 "first_name": "Sanjiv",
#                 "last_name": "Sabarwal",
#                 "email": "sales@vekaria.com",
#                 "mobile_no": "9909921851",
#             },
#             {
#                 "username": "HEMAT",
#                 "password": "PLN#0104",
#                 "first_name": "Hemat",
#                 "last_name": "Nandaniya",
#                 "email": "planning.vekaria@gmail.com",
#                 "mobile_no": "9998467101",
#             },
#             {
#                 "username": "NAIR",
#                 "password": "MN#1004",
#                 "first_name": "Manoj",
#                 "last_name": "Nair",
#                 "email": "hr1@vekaria.com",
#                 "mobile_no": "9909908016",
#             },
#             {
#                 "username": "HITESH",
#                 "password": "1963",
#                 "first_name": "Hitesh",
#                 "last_name": "Vekaria",
#                 "email": "it2@vekaria.com",
#                 "mobile_no": "9998471444",
#             },
#             {
#                 "username": "ACCOUNTS",
#                 "password": "acc#2904",
#                 "first_name": "Accounts",
#                 "last_name": "Vekaria",
#                 "email": "account@vekaria.com",
#                 "mobile_no": "9909908013",
#             },
#             {
#                 "username": "umang",
#                 "password": "IM#2705",
#                 "first_name": "Umang",
#                 "last_name": "Mehta",
#                 "email": "im@vekaria.com",
#                 "mobile_no": "9825255105",
#             },
#             {
#                 "username": "pratik",
#                 "password": "QC#1809",
#                 "first_name": "Pratik",
#                 "last_name": "Bhatt",
#                 "email": "pratikbhatt@vekaria.com",
#                 "mobile_no": None,
#             },
#             {
#                 "username": "KUNAL",
#                 "password": "AV#1204",
#                 "first_name": "Kunal",
#                 "last_name": "Vyas",
#                 "email": "av@vekaria.com",
#                 "mobile_no": "8141566363",
#             },
#             {
#                 "username": "DHAVAL",
#                 "password": "vekaria",
#                 "first_name": "Dhaval",
#                 "last_name": "Pandya",
#                 "email": "comp.vekaria@gmail.com",
#                 "mobile_no": "9979788686",
#             },
#         ]
#         for userdate in udata:
#             print(userdate['mobile_no'])
#             user = User.objects.create(email=userdate['email'],username=userdate['username'],first_name=userdate['first_name'],last_name=userdate['last_name'])
#             print(user.id)
#             Auth=AuthUser.objects.filter(id=user.id).update(creation_by=1,mobile_no=userdate['mobile_no'])
#             user.set_password(userdate['password'])
#             user.save()
#             # print(user['username'])

#         return super().get(request, *args, **kwargs)
