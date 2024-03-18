
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from vekaria_erp import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/',include('authuser.urls')), 
    path('api/v1/inventory/',include('inventory_and_stores.urls')),
    path('api/v1/supplychain/',include('supply_chain.urls')),
    path('api/v1/notification/',include('notification.urls')),
    path('api/v1/masterdata/',include('masterdata.urls')),
    path('api/v1/sales/',include('sales.urls')),
    path('api/v1/qc/',include('qc_reports.urls'))     

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   
   