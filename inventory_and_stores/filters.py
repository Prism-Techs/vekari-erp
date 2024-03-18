import django_filters
from .models import PartsMaster

class PartsMasterFilter(django_filters.FilterSet):
    product_part_name = django_filters.CharFilter(lookup_expr='icontains')
    product_part_no = django_filters.CharFilter(lookup_expr='icontains')
    category__c_name = django_filters.CharFilter(lookup_expr='icontains', field_name='category__c_name')
    product_source_type = django_filters.CharFilter(lookup_expr='icontains', field_name='product_source_type')

    class Meta:
        model = PartsMaster
        fields = []
