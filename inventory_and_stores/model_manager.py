from django.db import models


class ActivePartsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class AllPartsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

class ActiveSubPartsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(part_is_active=True)

class AllSubPartsManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    
class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)

class AllManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()
    

