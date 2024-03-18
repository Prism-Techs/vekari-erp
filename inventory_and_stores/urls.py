from django.urls import path
from .views import  *
urlpatterns = [ 
    # admin 
    path('allparts', AllPartAPIView.as_view(), name='parts-list-create'),
    path('allparts/<int:part_id>/', AllPartRetrieveAPIView.as_view(), name='parts-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('allvendor', AllVendorsAPIView.as_view(), name='vendor-list-create'),  # List and Create
    path('allvendor/<int:pk>/', AllVendorsRetrieveAPIView.as_view(), name='vendor-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('allsource', AllSourceAPIView.as_view(), name='source-list-create'),  # List and Create
    path('allsource/<int:pk>/', AllSourceRetrieveAPIView.as_view(), name='source-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('allcategory', AllCategoryAPIView.as_view(), name='source-list-create'),  # List and Create
    path('allcategory/<int:pk>/', AllCategoryRetrieveAPIView.as_view(), name='source-retrieve-update-destroy'),  # Retrieve, Update, Destroy



    path('subparts/<int:part_id>/', SubPartListAPIView.as_view(), name='parts-list-create'),  # List and Create
    path('parts', PartAPIView.as_view(), name='parts-list-create'),
    path('parts/<int:part_id>/', PartRetrieveAPIView.as_view(), name='parts-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path("subpart/<int:pk>/", SubPartAPIView.as_view(), name=""),
    path('assembly', AssemblyAPIView.as_view(), name='assembly-list-create'),  # List and Create
    path('assembly/<int:part_id>/', AssemblyRetrieveAPIView.as_view(), name='assembly-retrieve-update-destroy'),  # Retrieve, Update, Destroy 
    path('machine', MachineAPIView.as_view(), name='machine-list-create'),  # List and Create
    path('machine/<int:part_id>/', MachineRetrieveAPIView.as_view(), name='machine-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('source', SourceAPIView.as_view(), name='source-list-create'),  # List and Create
    path('source/<int:pk>/', SourceRetrieveAPIView.as_view(), name='source-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('category', CategoryAPIView.as_view(), name='source-list-create'),  # List and Create
    path('category/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='source-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('vendor', VendorsAPIView.as_view(), name='vendor-list-create'),  # List and Create
    path('vendor/<int:pk>/', VendorsRetrieveAPIView.as_view(), name='vendor-retrieve-update-destroy'),  # Retrieve, Update, Destroy
    path('partsvendors', PartsVendorsAPIView.as_view(), name='partsvendor-list-create'),  # List and Create
    path('partsvendors/<int:pk>/', PartsVendorsAPIViewRetrieveAPIView.as_view(), name='partsvendor-retrieve-update-destroy'),
    path('getpartsvendors/<int:pk>/', GetPartsVendorAPIView.as_view(), name='partsvendor-get'),
    path('inward',Purch_InwardAPIView.as_view(),name="create-inward"),
    path('inward/<int:pk>/',Purch_InwardRetrieveAPIView.as_view(),name='inward-update-destroy'),
    path('shopfloor',ShopfloorAPIView.as_view(),name="create-inward"),
    path('shopfloor/<int:pk>/',ShopfloorRetrieveAPIView.as_view(),name='inward-update-destroy'),
    path("machine", MachineAPIView.as_view(), name="machine-create-get"),
    path("machine/<int:pk>/", MachineRetrieveAPIView.as_view(), name="machine-update-destroy"),
    path("stock",StockAPIView.as_view(),name="stock-get"),
    path("stock/part",PartStockAPIView.as_view(),name="stock-get"),
    path("stock/assembly",AssemblyStockAPIView.as_view(),name="stock-get"),
    path("stock/material",Raw_MatStockAPIView.as_view(),name="stock-get"),
    path("stock/<int:pk>/",StockRetrieveAPIView.as_view(),name="stock-update-destroy"),
    path("stock_reserve",ReserveStockAPIView.as_view(),name="stock-get"),
    path("stock_reserve/part",PartReserveStockAPIView.as_view(),name="stock-get"),
    path("stock_reserve/assembly",AssemblyReserveStockAPIView.as_view(),name="stock-get"),
    path("stock_reserve/material",MaterialReserveStockAPIView.as_view(),name="stock-get"),
    path("stock_reserve/<int:pk>/",ReserveStockRetrieveAPIView.as_view(),name="stock-update-destroy"),
    path("raw_material",RawMaterialAPIView.as_view(),name="material-create-get"),
    path("raw_material/<int:pk>/",RawMaterialRetrieveAPIView.as_view(),name="material-update-destroy"),
    path("mrs",MrsAPIView.as_view(),name="mrs-create-get"),    
    path("mrs/pending",MrsPendingAPIView.as_view(),name="mrs-pending-create-get"),    
    path("mrs/last",MrLastAPIView.as_view(),name="mrs-no"), 
    path("mrs/<slug:mrs_no>/",MrsRetrieveAPIView.as_view(),name="mrs-update-destroy"),   
    path("min",MinAPIView.as_view(),name="mrs-create-get"), 
    path("min/issued",MinIssuedAPIView.as_view(),name="mrs-create-get"), 
    path("min/last",MinLastAPIView.as_view(),name="mrs-no"), 
    path("min/<slug:mrs_no>/",MinRetrieveAPIView.as_view(),name="mrs-update-destroy"),         
    path("cis",CISAPIView.as_view(),name="cis-create"),         
    path("cis/last",CisLastAPIView.as_view(),name="cis-get"),         
    path("department",DepartmentAPIView.as_view(),name="dept-create-get"),
    path("department/<int:pk>/",DepartmentRetrieveAPIView.as_view(),name="dept-update-destroy"),

    
    path("purch_requistion",PurchRequistAPIView.as_view(),name="purch_requistion-update-destroy"),
    path("purch_requistion/last",PurchrequistLastAPIView.as_view(),name="purch_requistion-update-destroy"),
    path("purch_requistion/<int:pk>/",PurchRequistRetrieveAPIView.as_view(),name="purch_requistion-update-destroy"),
    path("purch_requistion/return/<int:pk>/",PurchRequistReturnRetrieveAPIView.as_view(),name="purch_requistion-update-destroy"),
    
    path('shopfloor/approval/<int:mat_sf_id>/',Shpofloor_ApproverRetrieveAPIView.as_view(),name='shop_floor_approval'),
    path('shopfloor/return/<int:mat_sf_id>/',ShpofloorReturnRetrieveAPIView.as_view(),name='shop_floor_approval'),

    path("rmvendor/",Raw_VendorAPIView.as_view(),name="rm-vendor"),
    path("rmvendor/<int:pk>/",Raw_UpdateVendorAPIView.as_view(),name="rm-vendor-update-destroy"),
    path('getrmvendors/<int:pk>/', GetRMVendorAPIView.as_view(), name='get-rm-vendor-get'),
    
    
    # path("vendorentry",vendorentry.as_view(),name="vendorentry"),
    # path("raw_mat_data",raw_mat_data.as_view(),name="raw_mat_data"),
    # path('createstock/', stockcreate.as_view(), name='part'),  # Retrieve, Update, Destroy
    # path('createstockrm/', stockrmcreate.as_view(), name='partist'),  # Retrieve, Update, Destroy
    # path('reservcreatestock/', Reservstockcreate.as_view(), name='partist'),  # Retrieve, Update, Destroy
    # path('reservRMcreatestock/', ReservRmstockcreate.as_view(), name='partist'),  # Retrieve, Update, Destroy
    # path('partlist/', partlist.as_view(), name='partist'),  # Retrieve, Update, Destroy
]                                                