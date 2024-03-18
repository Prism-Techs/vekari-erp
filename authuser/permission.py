from rest_framework import permissions, exceptions
from .models import *
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.exceptions import APIException, ValidationError, PermissionDenied
# from django.contrib.auth.models import Permission
def group_permissions(*group_names):
    def decorator(cls):
        cls.permission_classes = [IsAuthenticated, YourPermission]
        cls.group_permissions = group_names
        return cls
    return decorator
class YourPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        print(user)
       
        if user.is_superuser:
            return True  # success
        auth= AuthUser.objects.get(id=user.id)
        if auth.is_admin:
            return True  # success
        view_permission=[]
        change_permission=[]
        add_permission=[]
        delete_permission=[]
        # success
        # print(user.is_superuser)
        model_permissions = view.group_permissions

        for model in model_permissions:
            view_permission.append(
                UserPermission.objects.filter(
                    group__group_name=model,
                    user=user.id,
                    permission__permission_name="view"
                ).exists()
            )
            add_permission.append(
                UserPermission.objects.filter(
                    group__group_name=model,
                    user=user.id,
                    permission__permission_name="create"
                ).exists()
            )
            change_permission.append(
                UserPermission.objects.filter(
                    group__group_name=model,
                    user=user.id,
                    permission__permission_name="update"
                ).exists()
            )
            delete_permission.append(
                UserPermission.objects.filter(
                    group__group_name=model,
                    user=user.id,
                    permission__permission_name="delete"
                ).exists()
            )

        if request.method == 'GET':
            if True in view_permission:
                return True
        elif request.method == 'POST':
            if True in add_permission:
                return True
        elif request.method in ['PUT', 'PATCH']:
            if True in change_permission:
                return True
        elif request.method == 'DELETE':
            if True in delete_permission:
                return True
        else:
            raise PermissionDenied({"message":"You have not permission to perform this action."})   
        
        raise PermissionDenied({"message":"You have not permission to perform this action."})   