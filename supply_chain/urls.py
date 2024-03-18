
from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [   
path('pr_process',PR_APIView.as_view()),
path('pr_process/<int:pk>/',PR_RetrieveAPIView.as_view()),
path('getallpr_process',ALLPR_APIView.as_view()),
path('pr/users_lvl1',user_lvl1_APIView.as_view()),
path('pr/users_lvl2',user_lvl2_APIView.as_view()),
path('pr/approval/<int:pr_id>/',PR_ApproverRetrieveAPIView.as_view()),
path('rfq',RFQ_APIView.as_view()),
path('rfq/<int:rfq_id>/',RFQ_RetrieveAPIView.as_view()),
path("po", PO_APIView.as_view(), name=""),
path("po/<int:pk>/", PO_RetrieveAPIView.as_view(), name=""),
path("po/approval/<int:po_id>/", PO_ApproverRetrieveAPIView.as_view(), name=""),
path("po/approval/return/<int:po_id>/", PO_ReturnRetrieveAPIView.as_view(), name=""),
path('po/users_lvl1',PO_user_lvl1_APIView.as_view()),
path('po/users_lvl2',PO_user_lvl2_APIView.as_view()),


]