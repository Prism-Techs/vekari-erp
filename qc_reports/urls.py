from django.urls import path
from .views import *
from .excel_report.qc_report import ExcelQCReportView
urlpatterns = [
    path('report',QCReport_APIView.as_view()),
    path('report/<int:pk>/',QCReportRetrieve_APIView.as_view()),
    path('report/excel/<int:qcr_id>/',ExcelQCReportView.as_view()),

]
