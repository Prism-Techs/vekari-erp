from django.db import models
from inventory_and_stores.models import PurchRequistion,PurchRequistionDetails,PartsMaster, RawMaterialMaster,VendorsMaster

# Create your models here.
class PrProcessMaster(models.Model):
    prp_id = models.AutoField(primary_key=True)
    prp_no = models.CharField(max_length=70, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField(blank=True, null=True)
    created_by = models.IntegerField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pr_process_master'

class PrProcessDetails(models.Model):
    prpd_id = models.AutoField(primary_key=True)
    prp = models.ForeignKey(PrProcessMaster, models.DO_NOTHING)
    pr = models.ForeignKey(PurchRequistion, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'pr_process_details'


class RfqMaster(models.Model):
    rfq_id = models.AutoField(primary_key=True)
    rfq_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', )
    vendor = models.ForeignKey(VendorsMaster, models.DO_NOTHING,)
    created_by = models.IntegerField(blank=True, null=True)
    modify_by = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'rfq_master'


class RfqDetails(models.Model):
    rfqd_id = models.AutoField(primary_key=True)
    rfq = models.ForeignKey('RfqMaster', models.DO_NOTHING)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    part_qty = models.IntegerField()
    make = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    model = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    specification_text = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'rfq_details'




class PoMaster(models.Model):
    po_id = models.AutoField(primary_key=True)
    po_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    prp = models.ForeignKey('PrProcessMaster', models.DO_NOTHING)
    created_date = models.DateTimeField()
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    po_approval_level = models.IntegerField(blank=True, null=True)
    po_approval_lvl_1_users = models.IntegerField(blank=True, null=True)
    po_approval_lvl_2_users = models.IntegerField(blank=True, null=True)
    po_lvl_1_approved = models.BooleanField(blank=True, null=True, default=False)
    po_lvl_2_approved = models.BooleanField(blank=True, null=True, default=False)
    remarks = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    po_create_by = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'po_master' 

class PoDetails(models.Model):
    pod_id = models.AutoField(primary_key=True)
    po = models.ForeignKey(PoMaster, models.DO_NOTHING)
    pr = models.ForeignKey(PurchRequistion, models.DO_NOTHING)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING, blank=True, null=True)
    rm = models.ForeignKey(RawMaterialMaster, models.DO_NOTHING, blank=True, null=True)
    pr_req_qty = models.IntegerField()
    req_qty = models.IntegerField()
    vendor = models.ForeignKey(VendorsMaster, models.DO_NOTHING,blank=True, null=True)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS',blank=True, null=True)
    type = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'po_details'

