from django.urls import path

from .views import AddTrans, DMTReportList, LedgerList

app_name = 'trans'

urlpatterns = [
    path('add-trans/', AddTrans.as_view(), name="add_trans"),
    path('DMT-Report/', DMTReportList.as_view(), name="dmt_report"),
    path('Balance-Ledger/', LedgerList.as_view(), name="balance_ledger"),
    path('DMT-Report/', DMTReportList.as_view(), name="dmt_report"),
]