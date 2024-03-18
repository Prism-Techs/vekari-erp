from django.db import models
from inventory_and_stores.models import PartsMaster
from .models_manager import *
from django.utils.text import slugify
# Create your models here.
class InspectionTypeMaster(models.Model):
    inspt_type_id = models.AutoField(primary_key=True)
    inspt_name = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'inspection_type_master'
class QcMaster(models.Model):
    qc_id = models.AutoField(primary_key=True)
    part = models.ForeignKey(PartsMaster, models.DO_NOTHING)
    qc_no = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField()
    created_by = models.IntegerField()
    modify_by = models.IntegerField()
    modify_date = models.DateTimeField()
    is_remove = models.BooleanField(default=False)
    objects = QcMasterManager()
    allobjects = AllQcMasterManager()
    class Meta:
        managed = False
        db_table = 'qc_master'

class ToolsMaster(models.Model):
    tool_name = models.CharField(max_length=250, db_collation='SQL_Latin1_General_CP1_CI_AS')
    created_date = models.DateTimeField(auto_now_add=True)
    created_by = models.IntegerField(blank=True, null=True)
    modify_date = models.DateTimeField(auto_now=True)
    modify_by = models.IntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_remove = models.BooleanField(default=False)
    slug = models.SlugField(blank=True,null=True, max_length=250)  # Add a slug field
    allobjects=AllToolsMasterManager()
    objects=ToolsMasterManager()
   
    def save(self, *args, **kwargs):
        if not self.id:  # Only generate slug if it's not already set
            self.slug = None  # Clear the slug to avoid potential conflicts
            save=super().save(*args, **kwargs)  # Save the instance to generate the id
            ToolsMaster.objects.filter(id=self.id).update(slug= slugify(f"{self.id}-{self.tool_name}"))
            return save
        else:
            # If the instance is being updated, retain the existing slug
            self.slug = slugify(f"{self.id}-{self.tool_name}")
        
            return super().save(*args, **kwargs)  # Save the instance with the updated slug
    class Meta:
        db_table = 'tools_master'
        
class QcDetails(models.Model):
    qcd_id = models.AutoField(primary_key=True)
    qc = models.ForeignKey(QcMaster, models.DO_NOTHING)
    parameter_name = models.CharField(max_length=80, db_collation='SQL_Latin1_General_CP1_CI_AS')
    nominal_dimension = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tolerance_positive = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tolerance_negative = models.CharField(max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    tolerance_tool_other = models.ForeignKey(ToolsMaster, models.DO_NOTHING, db_column='tolerance_tool_other', blank=True, null=True)
    uom = models.CharField(db_column='UOM', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    inspt_type = models.ForeignKey(InspectionTypeMaster, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'qc_details'
