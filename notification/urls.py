from django.urls import path
from .views import  *
urlpatterns = [ 

    path("", NotificationAPIView.as_view(), name="notification"),
    path("<int:pk>/", NotificationRetrieveAPIView.as_view(), name="retrieve_notification"),
    path("read/<int:pk>/", NotificationReadAPIView.as_view(), name="Read_notification")
]