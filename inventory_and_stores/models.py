# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from typing import Iterable, Optional
from django.utils import timezone
from django.db import models
from notification.models import Notification
from authuser.models import AuthUser 
from .model_manager import *

class ErpCitymaster(models.Model):
    cm_cityid = models.AutoField(db_column='CM_CityID', primary_key=True)  # Field name made lowercase.
    cm_cityname = models.CharField(db_column='CM_CityName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sm_stateid = models.IntegerField(db_column='SM_StateID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_CityMaster'


class ErpCustomercategory(models.Model):
    cc_categoryid = models.AutoField(db_column='CC_CategoryID', primary_key=True)  # Field name made lowercase.
    cc_categoryname = models.CharField(db_column='CC_CategoryName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cc_isactive = models.IntegerField(db_column='CC_IsActive', blank=True, null=True)  # Field name made lowercase.
    cc_createdate = models.DateTimeField(db_column='CC_CreateDate', blank=True, null=True)  # Field name made lowercase.
    cc_modifydate = models.DateTimeField(db_column='CC_ModifyDate', blank=True, null=True)  # Field name made lowercase.
    um_userid = models.IntegerField(db_column='UM_UserID', blank=True, null=True)  # Field name made lowercase.
    cc_isparcelcategory = models.IntegerField(db_column='CC_IsParcelCategory', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_CustomerCategory'


class ErpCustomermaster(models.Model):
    cm_customerid = models.AutoField(db_column='CM_CustomerID', primary_key=True)  # Field name made lowercase.
    cm_customername = models.CharField(db_column='CM_CustomerName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_addressline1 = models.CharField(db_column='CM_AddressLine1', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_addressline2 = models.CharField(db_column='CM_AddressLine2', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_addressline3 = models.CharField(db_column='CM_AddressLine3', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_addressline4 = models.CharField(db_column='CM_AddressLine4', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_cityid = models.IntegerField(db_column='CM_CityID', blank=True, null=True)  # Field name made lowercase.
    cm_pincode = models.CharField(db_column='CM_Pincode', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sm_stateid = models.IntegerField(db_column='SM_StateID', blank=True, null=True)  # Field name made lowercase.
    cm_countryid = models.IntegerField(db_column='CM_CountryID', blank=True, null=True)  # Field name made lowercase.
    sm_statecode = models.CharField(db_column='SM_StateCode', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_phoneoffice = models.CharField(db_column='CM_PhoneOffice', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_faxoffice = models.CharField(db_column='CM_FaxOffice', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_phoneresidency = models.CharField(db_column='CM_PhoneResidency', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_mobile = models.CharField(db_column='CM_Mobile', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_email = models.CharField(db_column='CM_Email', max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_website = models.CharField(db_column='CM_Website', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_category = models.CharField(db_column='CM_Category', max_length=25, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_gstno = models.CharField(db_column='CM_GSTNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_bankaccname = models.CharField(db_column='CM_BankAccName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_bankaccno = models.CharField(db_column='CM_BankAccNo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_ifscode = models.CharField(db_column='CM_IFSCode', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_bankname = models.CharField(db_column='CM_BankName', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_isactive = models.IntegerField(db_column='CM_IsActive', blank=True, null=True)  # Field name made lowercase.
    um_userid = models.IntegerField(db_column='UM_UserID', blank=True, null=True)  # Field name made lowercase.
    cm_createdate = models.DateTimeField(db_column='CM_CreateDate', blank=True, null=True)  # Field name made lowercase.
    cm_modifydate = models.DateTimeField(db_column='CM_ModifyDate', blank=True, null=True)  # Field name made lowercase.
    cm_ipaddress = models.CharField(db_column='CM_IPAddress', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_contactperson = models.CharField(db_column='CM_ContactPerson', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_designation = models.CharField(db_column='CM_Designation', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cc_categoryid = models.IntegerField(db_column='CC_CategoryID', blank=True, null=True)  # Field name made lowercase.
    cm_remarks = models.CharField(db_column='CM_Remarks', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cm_isprime = models.IntegerField(db_column='CM_IsPrime', blank=True, null=True)  # Field name made lowercase.
    cm_panno = models.CharField(db_column='CM_PANNo', max_length=15, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_CustomerMaster'

class ErpProductmaster(models.Model):
    pm_productid = models.AutoField(db_column='PM_ProductID', primary_key=True)  # Field name made lowercase.
    pm_productcode = models.CharField(db_column='PM_ProductCode', max_length=100, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    pm_productname = models.CharField(db_column='PM_ProductName', max_length=200, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    pm_productdesc = models.CharField(db_column='PM_ProductDesc', max_length=500, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    pm_rate = models.DecimalField(db_column='PM_Rate', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pm_image = models.BinaryField(db_column='PM_Image', blank=True, null=True)  # Field name made lowercase.
    pm_producttype = models.IntegerField(db_column='PM_ProductType', blank=True, null=True)  # Field name made lowercase.
    pm_isactive = models.IntegerField(db_column='PM_IsActive', blank=True, null=True)  # Field name made lowercase.
    um_userid = models.IntegerField(db_column='UM_UserID', blank=True, null=True)  # Field name made lowercase.
    pm_createdate = models.DateTimeField(db_column='PM_CreateDate', blank=True, null=True)  # Field name made lowercase.
    pm_modifydate = models.DateTimeField(db_column='PM_ModifyDate', blank=True, null=True)  # Field name made lowercase.
    pm_ipaddress = models.CharField(db_column='PM_IPAddress', max_length=60, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    pm_hsmnumber = models.CharField(db_column='PM_HSMNumber', max_length=30, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    pm_drawbackno = models.CharField(db_column='PM_DrawbackNo', max_length=30, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    pm_imageurl = models.CharField(db_column='PM_ImageURL', max_length=500, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_ProductMaster'
        
class CategoryMaster(models.Model):
    category_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=80, db_collation='Latin1_General_CI_AI')
    create_by = models.IntegerField()
    create_date = models.DateTimeField()
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField()
    closed_by = models.IntegerField(blank=True, null=True)
    objects = ActiveManager()  # Default manager for active parts
    all_objects = AllManager() 
    class Meta:
        managed = False
        db_table = 'category_master'


class PartsMaster(models.Model):
    part_id = models.AutoField(primary_key=True)
    product_part_no = models.CharField(max_length=70, db_collation='Latin1_General_CI_AI')
    product_part_name = models.TextField(db_collation='Latin1_General_CI_AI')
    product_descp = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    uom = models.CharField(db_column='UOM', max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    category = models.ForeignKey(CategoryMaster, models.DO_NOTHING, blank=True, null=True)
    product_pic_url = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    product_cost = models.DecimalField(max_digits=18, decimal_places=0,blank=True, null=True)
    source = models.ForeignKey('SourceMaster', models.DO_NOTHING, blank=True, null=True)
    product_source_type =models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    product_drawing_no = models.CharField(max_length=80, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    drawing_img = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    drawback_no = models.CharField(max_length=80, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    minimum_stock_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    hsn_code = models.CharField(max_length=80, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    material_type = models.CharField(max_length=80, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    drawback_no = models.CharField(max_length=10, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    create_by = models.IntegerField()
    create_date = models.DateTimeField()
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    aproved_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    # specification_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    # specification_upload = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    
    
    objects = ActivePartsManager()  # Default manager for active parts
    all_objects = AllPartsManager()  # Manager for all parts including inactive ones
    class Meta:
        managed = False
        db_table = 'parts_master'
class VendorsMaster(models.Model):
    vendor_id = models.AutoField(primary_key=True)
    vendor_name = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')
    vendor_email = models.CharField(max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_gst = models.CharField(db_column='vendor_GST', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    vendor_address = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_address_2 = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_address_3 = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_address_4 = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_pin_code = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)
    vendor_bank_name = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_ifsc_code = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_account_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    vendor_city = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_mobile = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_contact_list = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_contact2 = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_mobile2 = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    vendor_contact3 = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_mobile3 = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()
    objects = ActiveManager()  # Default manager for active parts
    all_objects = AllManager() 
    class Meta:
        managed = False
        db_table = 'vendors_master'

class PartsVendorsMaster(models.Model):
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    vendor = models.ForeignKey(VendorsMaster, models.DO_NOTHING)
    part_vendor_make = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    part_vendor_model = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    part_vendor_datasheet_url = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    part_vendor_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    part_vendor_min_order_qty = models.DecimalField(db_column='part_vendor_Min_Order_qty', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    part_vendor_lead_time = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    catalog_url = models.TextField(  db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    quotation_url = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)  # Field name made lowercase.
    is_active = models.BooleanField(default=True)

    objects = ActiveManager()  # Default manager for active parts
    all_objects = AllManager() 
    class Meta:
        managed = False
        db_table = 'parts_vendors_master'

class SourceMaster(models.Model):
    s_name = models.CharField(db_column='S_name', max_length=90, db_collation='Latin1_General_CI_AI')  # Field name made lowercase.
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()

    objects = ActiveManager()  # Default manager for active parts
    all_objects = AllManager() 
    class Meta:
        managed = False
        db_table = 'source_master'


class StoreLocation(models.Model):
    store_location_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    row_no = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    rack_no = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    shelf_no = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    tub_no = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    remark = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_location'


class SubpartMaster(models.Model):
    subpart_master_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING,related_name="sub_part_id")
    sub_part = models.ForeignKey(PartsMaster, models.DO_NOTHING,related_name="sub_subpart_id")
    sub_part_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    subpart_type = models.IntegerField(blank=True, null=True)
    subpart_subtype = models.IntegerField(blank=True, null=True)
    part_is_active = models.BooleanField(blank=True, null=True,)
    created_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now,blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    objects = ActiveSubPartsManager()  # Default manager for active parts
    all_objects = AllSubPartsManager()
    class Meta:
        managed = False
        db_table = 'subpart_master'





class DepartmentMaster(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=90, db_collation='SQL_Latin1_General_CP1_CI_AS')
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department_master'

class PurchMaster(models.Model):
    mat_iw_id = models.AutoField(primary_key=True)
    mrr_no = models.IntegerField()
    vendor = models.ForeignKey('VendorsMaster', models.DO_NOTHING, blank=True, null=True)
    vendor_po = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    vendor_inv_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    invoice_dt = models.DateField(blank=True, null=True)
    net_val = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    cgst_amt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    sgst_amt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    igst_amt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    frght_chrgs = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    frwd_chrgs = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    other_chrgs = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    dis_amt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    dis_per = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    gross_val = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    inv_url = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    lr_url = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)
    inv_chk = models.BooleanField(blank=True, null=True)
    inspt_chk = models.BooleanField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(db_collation='Latin1_General_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_master'

class PurchDetails(models.Model):
    pd_id = models.AutoField(primary_key=True)
    mat_iw = models.ForeignKey(PurchMaster, models.DO_NOTHING)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    ord_qty = models.IntegerField(blank=True, null=True)
    recd_qty = models.IntegerField(blank=True, null=True)
    rej_qty = models.IntegerField(blank=True, null=True)
    unit_rate = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    disc_amt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    gst_per = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)
    qc_reqd = models.BooleanField(blank=True, null=True)
    amt = models.DecimalField(max_digits=20, decimal_places=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_details'






class ShopFloorMaster(models.Model):
    mat_sf_id = models.AutoField(primary_key=True)
    rts_no=models.CharField(max_length=50,db_collation='Latin1_General_CI_AI', blank=True, null=True)
    min_no = models.IntegerField()
    from_department = models.ForeignKey(DepartmentMaster, models.DO_NOTHING, blank=True, null=True)
    prepared_by = models.IntegerField(blank=True, null=True)
    auth_by = models.IntegerField(blank=True, null=True)
    issued_by = models.IntegerField(blank=True, null=True)
    inspt_chk = models.BooleanField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.CharField(max_length=50,db_collation='Latin1_General_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_floor_master'

class ShopFloorDetails(models.Model):
    sfd_id = models.AutoField(primary_key=True)
    mat_sf = models.ForeignKey(ShopFloorMaster, models.DO_NOTHING, blank=True, null=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rtn_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    ref_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    uom = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='Latin1_General_CI_AI', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_floor_details'


# class RawMaterialMaster(models.Model):
#     rm_id = models.AutoField(primary_key=True)
#     rm_mat_name = models.CharField(max_length=90, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     rm_mat_code = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS',blank=True, null=True)
#     rm_mat_desc = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
#     rm_sec_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     rm_size = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     uom = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
#     rm_stock_free = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
#     rm_stock_res = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
#     create_by = models.IntegerField(blank=True, null=True)
#     created_date = models.DateTimeField(blank=True, null=True)
#     modify_by = models.IntegerField(blank=True, null=True)
#     modify_date = models.DateTimeField(blank=True, null=True)

#     class Meta:
#         managed = False
#         db_table = 'raw_material_master'

class RawMaterialMaster(models.Model):
    rm_id = models.AutoField(primary_key=True)
    rm_mat_name = models.CharField(max_length=90, db_collation='SQL_Latin1_General_CP1_CI_AS')
    rm_mat_code = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_mat_desc = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_sec_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    rm_size = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    hsn_code = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    rm_stock_free = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    rm_stock_res = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    uom = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    rm_image = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    drawing_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'raw_material_master'


class StockMaster(models.Model):
    stock_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING, blank=True, null=True)
    stock_avail = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    stock_ui = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stock_reserv = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stock_rej = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    updt_by = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_master'

   
class StockReserv(models.Model):
    stock_reserv_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING, blank=True, null=True)
    reserve_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    reserve_date = models.DateTimeField(blank=True, null=True)
    issue_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    issue_date = models.DateTimeField(blank=True, null=True)
    reserve_by = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_reserv'


class StockUpdate(models.Model):
    stock_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING, blank=True, null=True)
    tran_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    doc_ref = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stock_avail = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    stock_ui = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stock_reserv = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    stock_rej = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    updt_date = models.DateTimeField(blank=True, null=True)
    updt_by = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_update'







class MrsMaster(models.Model):
    mrs_id = models.AutoField(primary_key=True)
    mrs_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    min_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mrs_date = models.DateTimeField(blank=True, null=True)
    part = models.ForeignKey('PartsMaster', models.DO_NOTHING, blank=True, null=True)
    req_qty = models.IntegerField(blank=True, null=True)
    issue_qty = models.IntegerField(blank=True, null=True)
    from_dept = models.ForeignKey(DepartmentMaster, models.DO_NOTHING, db_column='from_dept', blank=True, null=True)
    prep_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    auth_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    issue_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remark = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    type = models.BooleanField(blank=True, null=True)
    status = models.BooleanField(blank=True, null=True)
    is_close = models.BooleanField(blank=True, null=True,default=False)

    class Meta:
        managed = False
        db_table = 'mrs_master'



class MrsDetails(models.Model):
    mrs_detail_id = models.AutoField(primary_key=True)
    mrs = models.ForeignKey('MrsMaster', models.DO_NOTHING)
    rm = models.ForeignKey('RawMaterialMaster', models.DO_NOTHING, blank=True, null=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    req_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    issue_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'mrs_details'





class MatRetnStorMaster(models.Model):
    mat_retn_stor_id = models.IntegerField(primary_key=True)
    from_department = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    min_no = models.CharField(max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    prep_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    auth_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    issued_by = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    insp_req = models.BooleanField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'mat_retn_stor_master'

class MatRetnStorDetail(models.Model):
    mat_retn_str_det_id = models.IntegerField(primary_key=True)
    mat_retn_stor = models.ForeignKey(MatRetnStorMaster, models.DO_NOTHING) 
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    description = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rtn_qty = models.IntegerField(blank=True, null=True)
    ion_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    uom = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ref_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'mat_retn_stor_detail'

class PurchRequistion(models.Model):
    pr_id = models.AutoField(primary_key=True)
    pr_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    pr_date = models.DateField(blank=True, null=True)
    dept = models.ForeignKey(DepartmentMaster, models.DO_NOTHING, blank=True, null=True)
    req_by_date = models.DateField(blank=True, null=True)
    pr_create_by = models.IntegerField(blank=True, null=True)
    pr_approval_level = models.IntegerField(blank=True, null=True)
    pr_approval_lvl_1_users = models.IntegerField(db_column='pr_approval_lvl_1_users')  # Field renamed because it contained more than one '_' in a row.
    pr_approval_lvl_2_users = models.IntegerField(db_column='pr_approval_lvl_2_users', blank=True, null=True)  # Field renamed because it contained more than one '_' in a row.
    pr_lvl_1_approved = models.BooleanField()
    pr_lvl_2_approved = models.BooleanField()
    pr_status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remarks=models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'purch_requistion'
    def save(self, *args, **kwargs):
        is_new = self.pk is not None 
      
        super().save(*args, **kwargs)
        if not is_new:
            print("+++++++ create PurchRequistion +++++++",is_new,self.pk)
            if self.pr_approval_level == 1:
                notification_message = f"A purchase requisition with the code {self.pr_no} has been generated. Please click here to approve the PR."  

                notification_user = AuthUser.objects.get(pk=self.pr_approval_lvl_1_users)
                notification = Notification.objects.create(
                    type='PR_Approval',
                    message=notification_message,
                    created_date=timezone.now(),
                    sender_user_id=self.pr_create_by,
                    receiver_user=notification_user,
                    action=self.pr_id,
                    is_read=False
                )
            if self.pr_approval_level == 2:
                notification_message = f"A purchase requisition with the code {self.pr_no} has been generated. Please click here to approve the PR."  

                notification_user = AuthUser.objects.get(pk=self.pr_approval_lvl_1_users)
                notification = Notification.objects.create(
                    type='PR_Approval',
                    message=notification_message,
                    created_date=timezone.now(),
                    receiver_user=notification_user,
                    sender_user_id=self.pr_create_by,
                    action=self.pr_id,
                    is_read=False
                )
        else:
            print("+++++++update PurchRequistion +++++++",is_new,self.pk)
        
            
        
class PurchRequistionDetails(models.Model):
    prd_id = models.AutoField(primary_key=True)
    pr = models.ForeignKey(PurchRequistion, models.DO_NOTHING, blank=True, null=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    part_qty = models.IntegerField(blank=True, null=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING, blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_requistion_details'



class RmStoreLocation(models.Model):
    store_location_rm_id = models.AutoField(primary_key=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING)
    rm_row_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_rack_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_shelf_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_tub_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remark = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rm_store_location'

class RmVendorMaster(models.Model):
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING)
    vendor = models.ForeignKey(VendorsMaster, models.DO_NOTHING)
    rm_vendor_make = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_vendor_model = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_vendor_datasheet_url = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_vendor_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    rm_vendor_min_order_qty = models.IntegerField(blank=True, null=True)
    rm_vendor_lead_time = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    catalog_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    quotation_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'rm_vendor_master'