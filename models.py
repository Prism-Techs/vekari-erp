# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class ErpProductaccessory(models.Model):
    pa_id = models.AutoField(db_column='PA_ID', primary_key=True)  # Field name made lowercase.
    pa_productid = models.IntegerField(db_column='PA_ProductID', blank=True, null=True)  # Field name made lowercase.
    pa_subproductid = models.IntegerField(db_column='PA_SubProductID', blank=True, null=True)  # Field name made lowercase.
    pa_quantity = models.IntegerField(db_column='PA_Quantity', blank=True, null=True)  # Field name made lowercase.
    pa_isactive = models.IntegerField(db_column='PA_IsActive', blank=True, null=True)  # Field name made lowercase.
    um_userid = models.IntegerField(db_column='UM_UserID', blank=True, null=True)  # Field name made lowercase.
    pa_createdate = models.DateTimeField(db_column='PA_CreateDate', blank=True, null=True)  # Field name made lowercase.
    pa_modifydate = models.DateTimeField(db_column='PA_ModifyDate', blank=True, null=True)  # Field name made lowercase.
    pa_type = models.IntegerField(db_column='PA_Type', blank=True, null=True)  # Field name made lowercase.
    pa_sort = models.IntegerField(db_column='PA_Sort', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_ProductAccessory'


class ErpProductmaster(models.Model):
    pm_productid = models.AutoField(db_column='PM_ProductID', primary_key=True)  # Field name made lowercase.
    pm_productcode = models.CharField(db_column='PM_ProductCode', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pm_productname = models.CharField(db_column='PM_ProductName', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pm_productdesc = models.CharField(db_column='PM_ProductDesc', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pm_rate = models.DecimalField(db_column='PM_Rate', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    pm_image = models.BinaryField(db_column='PM_Image', blank=True, null=True)  # Field name made lowercase.
    pm_producttype = models.IntegerField(db_column='PM_ProductType', blank=True, null=True)  # Field name made lowercase.
    pm_isactive = models.IntegerField(db_column='PM_IsActive', blank=True, null=True)  # Field name made lowercase.
    um_userid = models.IntegerField(db_column='UM_UserID', blank=True, null=True)  # Field name made lowercase.
    pm_createdate = models.DateTimeField(db_column='PM_CreateDate', blank=True, null=True)  # Field name made lowercase.
    pm_modifydate = models.DateTimeField(db_column='PM_ModifyDate', blank=True, null=True)  # Field name made lowercase.
    pm_ipaddress = models.CharField(db_column='PM_IPAddress', max_length=60, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pm_hsmnumber = models.CharField(db_column='PM_HSMNumber', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pm_drawbackno = models.CharField(db_column='PM_DrawbackNo', max_length=30, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    pm_imageurl = models.CharField(db_column='PM_ImageURL', max_length=500, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_ProductMaster'


class ErpSubproductmaster(models.Model):
    spm_id = models.AutoField(db_column='SPM_ID', primary_key=True)  # Field name made lowercase.
    spm_productid = models.IntegerField(db_column='SPM_ProductID', blank=True, null=True)  # Field name made lowercase.
    spm_subproductid = models.IntegerField(db_column='SPM_SubProductID', blank=True, null=True)  # Field name made lowercase.
    spm_isactive = models.IntegerField(db_column='SPM_IsActive', blank=True, null=True)  # Field name made lowercase.
    um_userid = models.IntegerField(db_column='UM_UserID', blank=True, null=True)  # Field name made lowercase.
    spm_createdate = models.DateTimeField(db_column='SPM_CreateDate', blank=True, null=True)  # Field name made lowercase.
    spm_modifydate = models.DateTimeField(db_column='SPM_ModifyDate', blank=True, null=True)  # Field name made lowercase.
    spm_quantity = models.IntegerField(db_column='SPM_Quantity', blank=True, null=True)  # Field name made lowercase.
    spm_productprice = models.DecimalField(db_column='SPM_ProductPrice', max_digits=10, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ERP_SubProductMaster'


class ApprovalMaster(models.Model):
    approval_id = models.AutoField(primary_key=True)
    approval_name = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'approval_master'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    mobile_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_admin = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    profile_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_ip_address = models.CharField(max_length=120, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    creation_by = models.IntegerField(blank=True, null=True)
    update_profile_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Authuser(models.Model):
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    mobile_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    is_superuser = models.BooleanField()
    is_staff = models.BooleanField()
    is_admin = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()
    profile_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_ip_address = models.CharField(max_length=120, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    creation_by = models.IntegerField(blank=True, null=True)
    update_profile_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'authuser'


class CategoryMaster(models.Model):
    category_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')
    create_by = models.IntegerField()
    create_date = models.DateTimeField()
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField()
    closed_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category_master'


class CompanyDetails(models.Model):
    companyname = models.CharField(db_column='companyName', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    companycity = models.CharField(db_column='companyCity', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    companyaddress = models.CharField(db_column='companyAddress', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    companycontact = models.CharField(db_column='companyContact', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    logo = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    modify_date = models.DateTimeField()
    modify_by = models.IntegerField()
    created_date = models.DateTimeField()
    created_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'company_details'


class DepartmentMaster(models.Model):
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(max_length=90, db_collation='SQL_Latin1_General_CP1_CI_AS')
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department_master'


class DespatchMaster(models.Model):
    nno = models.AutoField(db_column='NNO', primary_key=True)  # Field name made lowercase.
    cnam = models.CharField(db_column='CNAM', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ccity = models.CharField(db_column='CCITY', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cmachineno = models.CharField(db_column='CMACHINENO', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cmachno1 = models.IntegerField(db_column='CMACHNO1', blank=True, null=True)  # Field name made lowercase.
    cmachno2 = models.IntegerField(db_column='CMACHNO2', blank=True, null=True)  # Field name made lowercase.
    ndespachno = models.IntegerField(db_column='NDESPACHNO', blank=True, null=True)  # Field name made lowercase.
    ddespatcdt = models.DateField(db_column='DDESPATCDT', blank=True, null=True)  # Field name made lowercase.
    cextype = models.CharField(db_column='CEXTYPE', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cmodel = models.CharField(db_column='CMODEL', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cyear = models.CharField(db_column='CYEAR', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cremark = models.TextField(db_column='CREMARK', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    cremark1 = models.TextField(db_column='CREMARK1', db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    status = models.BooleanField(blank=True, null=True)
    is_delete = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'despatch_master'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class InspectionTypeMaster(models.Model):
    inspt_type_id = models.AutoField(primary_key=True)
    inspt_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'inspection_type_master'


class MrsDetails(models.Model):
    mrs_detail_id = models.AutoField(primary_key=True)
    mrs = models.ForeignKey('MrsMaster', models.DO_NOTHING)
    rm = models.ForeignKey('RawMaterialMaster', models.DO_NOTHING, blank=True, null=True)
    part = models.ForeignKey('PartsMaster', models.DO_NOTHING, blank=True, null=True)
    req_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    issue_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'mrs_details'


class MrsMaster(models.Model):
    mrs_id = models.AutoField(primary_key=True)
    mrs_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    min_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    mrs_date = models.DateTimeField(blank=True, null=True)
    part_id = models.IntegerField(blank=True, null=True)
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
    status = models.BooleanField()
    is_close = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'mrs_master'


class Notification(models.Model):
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    receiver_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    sender_user_id = models.IntegerField()
    action = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField()
    is_read = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'notification'


class PartsMaster(models.Model):
    part_id = models.AutoField(primary_key=True)
    product_part_no = models.CharField(max_length=70, db_collation='SQL_Latin1_General_CP1_CI_AS')
    product_part_name = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    product_descp = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    product_type = models.IntegerField(blank=True, null=True)
    uom = models.CharField(db_column='UOM', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    category = models.ForeignKey(CategoryMaster, models.DO_NOTHING, blank=True, null=True)
    product_pic_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    product_cost = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    source = models.ForeignKey('SourceMaster', models.DO_NOTHING, blank=True, null=True)
    product_source_type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    product_drawing_no = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    drawing_img = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    drawback_no = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    minimum_stock_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    hsm_code = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    material_type = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pm_drawback_no = models.CharField(max_length=10, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    aproved_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'parts_master'


class PartsVendorsMaster(models.Model):
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    vendor = models.ForeignKey('VendorsMaster', models.DO_NOTHING)
    part_vendor_make = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    part_vendor_model = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    part_vendor_datasheet_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    part_vendor_cost = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    part_vendor_min_order_qty = models.DecimalField(db_column='part_vendor_Min_Order_qty', max_digits=18, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    part_vendor_lead_time = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    catalog_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    quotation_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'parts_vendors_master'


class Permission(models.Model):
    permission_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'permission'


class PoDetails(models.Model):
    pod_id = models.AutoField(primary_key=True)
    po = models.ForeignKey('PoMaster', models.DO_NOTHING)
    pr = models.ForeignKey('PurchRequistion', models.DO_NOTHING)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    req_qty = models.IntegerField()
    pr_req_qty = models.IntegerField()
    vendor = models.ForeignKey('VendorsMaster', models.DO_NOTHING, blank=True, null=True)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'po_details'


class PoMaster(models.Model):
    po_id = models.AutoField(primary_key=True)
    po_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    prp = models.ForeignKey('PrProcessMaster', models.DO_NOTHING)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    po_approval_level = models.IntegerField(blank=True, null=True)
    po_approval_lvl_1_users = models.IntegerField(blank=True, null=True)
    po_approval_lvl_2_users = models.IntegerField(blank=True, null=True)
    po_lvl_1_approved = models.BooleanField(blank=True, null=True)
    po_lvl_2_approved = models.BooleanField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    po_create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'po_master'


class PrProcessDetails(models.Model):
    prpd_id = models.AutoField(primary_key=True)
    prp = models.ForeignKey('PrProcessMaster', models.DO_NOTHING)
    pr = models.ForeignKey('PurchRequistion', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pr_process_details'


class PrProcessMaster(models.Model):
    prp_id = models.AutoField(primary_key=True)
    prp_no = models.CharField(max_length=70, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'pr_process_master'


class PurchDetails(models.Model):
    pd_id = models.AutoField(primary_key=True)
    mat_iw = models.ForeignKey('PurchMaster', models.DO_NOTHING)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    recd_qty = models.IntegerField(blank=True, null=True)
    ord_qty = models.IntegerField(blank=True, null=True)
    rej_qty = models.IntegerField(blank=True, null=True)
    unit_rate = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    disc_amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    gst_per = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    qc_reqd = models.BooleanField(blank=True, null=True)
    amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_details'


class PurchMaster(models.Model):
    mat_iw_id = models.AutoField(primary_key=True)
    mrr_no = models.IntegerField()
    vendor = models.ForeignKey('VendorsMaster', models.DO_NOTHING, blank=True, null=True)
    vendor_po = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor_inv_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    invoice_dt = models.DateField(blank=True, null=True)
    net_val = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    cgst_amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    sgst_amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    igst_amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    frght_chrgs = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    frwd_chrgs = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    other_chrgs = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    dis_amt = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    dis_per = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    gross_val = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    inv_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    lr_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    inv_chk = models.BooleanField(blank=True, null=True)
    inspt_chk = models.BooleanField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_master'


class PurchRequistion(models.Model):
    pr_id = models.AutoField(primary_key=True)
    pr_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    pr_date = models.DateField(blank=True, null=True)
    dept = models.ForeignKey(DepartmentMaster, models.DO_NOTHING, blank=True, null=True)
    req_by_date = models.DateField(blank=True, null=True)
    pr_create_by = models.IntegerField(blank=True, null=True)
    pr_approval_level = models.IntegerField(blank=True, null=True)
    pr_approval_lvl_1_users = models.IntegerField(blank=True, null=True)
    pr_approval_lvl_2_users = models.IntegerField(blank=True, null=True)
    pr_lvl_1_approved = models.BooleanField()
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    pr_lvl_2_approved = models.BooleanField()
    pr_status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_requistion'


class PurchRequistionDetails(models.Model):
    prd_id = models.AutoField(primary_key=True)
    pr = models.ForeignKey(PurchRequistion, models.DO_NOTHING, blank=True, null=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    part_qty = models.IntegerField(blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'purch_requistion_details'


class QcDetails(models.Model):
    qcd_id = models.AutoField(primary_key=True)
    qc = models.ForeignKey('QcMaster', models.DO_NOTHING)
    parameter_name = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')
    nominal_dimension = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tolerance_positive = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    tolerance_negative = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    uom = models.CharField(db_column='UOM', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    inspt_type = models.ForeignKey(InspectionTypeMaster, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qc_details'


class QcMaster(models.Model):
    qc_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    qc_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField()
    created_by = models.IntegerField()
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField()
    is_remove = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'qc_master'


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


class RfqDetails(models.Model):
    rfqd_id = models.AutoField(primary_key=True)
    rfq = models.ForeignKey('RfqMaster', models.DO_NOTHING)
    part_id = models.IntegerField()
    part_qty = models.IntegerField()
    make = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    model = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    specification_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'rfq_details'


class RfqMaster(models.Model):
    rfq_id = models.AutoField(primary_key=True)
    rfq_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    vendor = models.ForeignKey('VendorsMaster', models.DO_NOTHING)
    created_by = models.IntegerField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rfq_master'


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
    vendor = models.ForeignKey('VendorsMaster', models.DO_NOTHING)
    rm_vendor_make = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_vendor_model = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_vendor_datasheet_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rm_vendor_cost = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    rm_vendor_min_order_qty = models.IntegerField(blank=True, null=True)
    rm_vendor_lead_time = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    catalog_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    quotation_url = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'rm_vendor_master'


class ShopFloorDetails(models.Model):
    sfd_id = models.AutoField(primary_key=True)
    mat_sf = models.ForeignKey('ShopFloorMaster', models.DO_NOTHING, blank=True, null=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rtn_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    ref_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    uom = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    ioa_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_floor_details'


class ShopFloorMaster(models.Model):
    mat_sf_id = models.AutoField(primary_key=True)
    rts_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    min_no = models.IntegerField()
    from_department = models.ForeignKey(DepartmentMaster, models.DO_NOTHING, blank=True, null=True)
    prepared_by = models.IntegerField(blank=True, null=True)
    auth_by = models.IntegerField(blank=True, null=True)
    issued_by = models.IntegerField(blank=True, null=True)
    inspt_chk = models.BooleanField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shop_floor_master'


class SourceMaster(models.Model):
    s_name = models.CharField(db_column='S_name', max_length=90, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField()
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    closed_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField()

    class Meta:
        managed = False
        db_table = 'source_master'


class StockMaster(models.Model):
    stock_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING, blank=True, null=True)
    stock_avail = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    stock_ui = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stock_reserv = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    stock_rej = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    last_update = models.DateTimeField(blank=True, null=True)
    updt_by = models.IntegerField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
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
    type = models.IntegerField(blank=True, null=True)
    updt_date = models.DateTimeField(blank=True, null=True)
    updt_by = models.IntegerField(blank=True, null=True)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stock_update'


class StoreLocation(models.Model):
    store_location_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    row_no = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    rack_no = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    shelf_no = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tub_no = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    remark = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'store_location'


class SubpartMaster(models.Model):
    subpart_master_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    sub_part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    sub_part_qty = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    subpart_type = models.IntegerField(blank=True, null=True)
    subpart_subtype = models.IntegerField(blank=True, null=True)
    part_is_active = models.BooleanField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subpart_master'


class UserApproval(models.Model):
    user_approval_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    approval = models.ForeignKey(ApprovalMaster, models.DO_NOTHING)
    approver_level = models.IntegerField(blank=True, null=True)
    create_by = models.IntegerField(blank=True, null=True)
    create_date = models.DateTimeField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_approval'


class UserPermission(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey('UserPermissionGroup', models.DO_NOTHING)
    permission_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user_permission'


class UserPermissionGroup(models.Model):
    group_name = models.CharField(unique=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'user_permission_group'


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
    vendor_account_no = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)
    vendor_ifsc_code = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'vendors_master'
