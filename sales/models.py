from django.db import models

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
