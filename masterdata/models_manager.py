
from django.db import models

class QcMasterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_remove=False)

class ToolsMasterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True,is_remove=False)
class AllQcMasterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_remove=False)
class AllToolsMasterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_remove=False)