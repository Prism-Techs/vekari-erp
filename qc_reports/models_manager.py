from django.db import models

class QcReportMasterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_delete=False)
class AllQcReportMasterManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()