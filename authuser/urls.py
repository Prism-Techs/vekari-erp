from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import *
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user',UserView.as_view(),name="user"),
    path('user/<int:pk>/',UserView.as_view(),name="user"),
    path('user/permission/<int:pk>/',PermissionView.as_view(),name="permission"),
    path('profile/',ProfileView.as_view(),name="profile"),
    path('profile/changepassword/',UserChangePassword.as_view(),name="changepassword"),
    path('NavPermission/',NavPermissionView.as_view(),name="permission"),
    path("allpermission/", AllpermissionView.as_view(), name=""),
    path("approval", ApprovalAPIView.as_view(), name=""),
    path("approval/permission/<int:userid>/", UserApprovalRetrieveAPIView.as_view(), name=""),
    path("approval/permission/", UserApprovalAPIView.as_view(), name=""),
    path("approval/<int:pk>/", ApprovalRetrieveAPIView.as_view(), name=""),
    path("sent-reset-password-email/",ResetPasswordEmailRequest.as_view()),
    path("reset-password/<uid>/<token>/",UserPasswordResetView.as_view()),
     path('activeusers',ActiveUsersView.as_view(),name="user"),
]