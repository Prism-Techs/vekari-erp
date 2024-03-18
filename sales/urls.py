from django.urls import path
from .views import  *
urlpatterns = [ 
    path("machinedispatch", MachineDispatchAPIView.as_view(), name="create-list-Matchinedispatch"),
    path("machinedispatch/<int:nno>", MachineDispatchRetrieveAPIView.as_view(), name="retrieve-update-destroy-Matchinedispatch"),
]