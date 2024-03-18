from django.urls import path
from .views import *
urlpatterns = [
    path("QC", QC_APIView.as_view(), name="QC_APIView"),
    path("QC/<int:pk>/", QC_RetrieveAPIView.as_view(), name="QC_RetrieveAPIView"),
    path("QC_Part", QC_search_APIView.as_view(), name="QC_SearchbypartAPIView"),
    path("inspection_type", Inspection_APIView.as_view(), name=""),
    path("part_bought-out", PartBoughtOut_APIView.as_view(), name=""),
    path('tools',tools_APIView.as_view(),name="get_create_tool"),
    path("tools/<slug:slug>/", tools_RetrieveAPIView.as_view(), name="update_delete_tools"),
    # admin 
    path('alltools',Alltools_APIView.as_view(),name="admin_get_create_tool"),
    path("alltools/<slug:slug>/", Alltools_RetrieveAPIView.as_view(), name="admin_update_delete_tools"),

]    