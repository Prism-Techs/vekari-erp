import django_filters
from qc_reports.models import * 
from django_filters import rest_framework as filter
from django.db.models import Q
from datetime import datetime
from django.utils.dateparse import parse_date
class QC_ReportFilter(django_filters.FilterSet):
    status= filter.CharFilter(lookup_expr='contains',field_name='status')
    search = filter.CharFilter(method='search_filter') 

    # # Ordering filter
    # order_by = filters.OrderingFilter(
    #     fields=(
    #         ('exp_date', 'exp_date'),
    #     )
    # )
    class Meta:
        model = QcReportsMaster
        fields = '__all__'
    
    def search_filter(self, queryset, name, value):
        # Filter by qcr_no, part__product_part_no, or status directly
        # Assuming value is a string that could represent a year, month, or day
        if len(value) == 4:  # Likely a year
            try:
                year = int(value)
                print(year)
                qs = queryset.filter(Q(created_date__year=year) )
            except ValueError:

                qs = queryset.filter(
                Q(qcr_no__icontains=value) | 
                Q(part__product_part_no__icontains=value) |
                Q(status__icontains=value)|
                Q(vendor__vendor_name__icontains=value)

                )
        elif len(value) == 2:  # Could be a month or a day
            try:
                month_or_day = int(value)
               
                qs = queryset.filter(Q(created_date__month=month_or_day) | Q(created_date__day=month_or_day))
            except ValueError:
                qs = queryset.filter(
                Q(qcr_no__icontains=value) | 
                Q(part__product_part_no__icontains=value) |
                Q(status__icontains=value)|
                Q(vendor__vendor_name__icontains=value)
            )
        else:
            qs = queryset.filter(
                Q(qcr_no__icontains=value) | 
                Q(part__product_part_no__icontains=value) |
                Q(status__icontains=value)|
                Q(vendor__vendor_name__icontains=value)

            )
            # Filter by qcr_no, part__product_part_no, or status directly if the value doesn't seem to be a date component
            try:
                # Check if 'value' can be parsed as a date
                datevalue= datetime.strptime(value, '%d-%m-%Y')
                print("date ",datevalue)
                # If yes, filter by created_date__date
                qs =  queryset.filter(created_date__date=datevalue)
            except ValueError as e:
                # print(e)
                pass
           
           
        

        return qs
       
      