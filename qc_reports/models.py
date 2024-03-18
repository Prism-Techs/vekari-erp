from django.db import models
from inventory_and_stores.models import PartsMaster,VendorsMaster
from masterdata.models import QcDetails
from .models_manager import *


class QcReportsMaster(models.Model):
    qcr_id = models.AutoField(primary_key=True)
    qcr_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    received_date = models.DateField(blank=True, null=True)
    qty = models.IntegerField()
    inspt_qty = models.IntegerField(default=0,blank=True, null=True)
    rejected_qty = models.IntegerField()
    qc_report_excel = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    vendor = models.ForeignKey(VendorsMaster, models.DO_NOTHING, blank=True, null=True)
    created_date = models.DateTimeField()
    created_by = models.IntegerField()
    modify_date = models.DateTimeField()
    modify_by = models.IntegerField()
    is_delete = models.BooleanField(default=False)
    status = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
   

    class Meta:
        managed = False
        db_table = 'qc_reports_master'



class QcReportsDetails(models.Model):
    qcrd_id = models.AutoField(primary_key=True)
    qc_id = models.IntegerField()
    qcr = models.ForeignKey(QcReportsMaster, models.DO_NOTHING)
    qcd = models.ForeignKey(QcDetails, models.DO_NOTHING)
    status=models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'qc_reports_details'



class QcReportsMeasued(models.Model):
    qcm_id = models.AutoField(primary_key=True)
    qcrd = models.ForeignKey(QcReportsDetails, models.DO_NOTHING)
    measured_dimensions = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS',blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qc_reports_measued'

