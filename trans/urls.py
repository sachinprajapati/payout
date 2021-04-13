from django.urls import path

from .views import *
app_name = 'trans'

urlpatterns = [
    path('add-trans/', AddTrans.as_view(), name="add_trans"),
    path('DMT-Report/', DMTReportList.as_view(), name="dmt_report"),
    path('Balance-Ledger/', LedgerList.as_view(), name="balance_ledger"),
    path('Account-Log/', AccountLogList.as_view(), name="account_log"),
    path('Add-Charges/', AddChargesView.as_view(), name="add_charges"),
    path('List-Charges/', ListChargesView.as_view(), name="list_charges"),
    path('Update-Charges/<int:pk>/', UpdateChargesView.as_view(), name="update_charges"),
    path('Add-Payment-Request/', AddPaymentRequestView.as_view(), name="add_request"),
    path('List-Payment-Request/', ListPaymentRequestView.as_view(), name="list_request"),
    path('All-Payment-Request/', AllPaymentRequestView.as_view(), name="all_request"),
    path('Update-Payment-Request/<int:pk>/', UpdatePaymentRequestView.as_view(), name="update_request"),
    path('Add-Bank/', AddBankView.as_view(), name="add_Bank"),
    path('List-Bank/', ListBankView.as_view(), name="list_Bank"),
    path('Update-Bank/<int:pk>/', UpdateBankView.as_view(), name="update_Bank"),
]