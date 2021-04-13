from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required

from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.export import TableExport

from .models import *
from .tables import *
from .forms import *
from django_filters.views import FilterView

def UserDecorator(function):
    def wrapper(request, *args, **kw):
        user=request.user
        if user.is_reseller or user.is_staff:
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        else:
            return function(request, *args, **kw)
    return wrapper

class AddTrans(CreateView):
    model = Transaction
    fields = "__all__"
    template_name = "form_view.html"

# @method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DMTReportList(ExportMixin, SingleTableMixin, FilterView):
    model = Transaction
    template_name = 'list_view.html'
    table_class = DMTTable
    filterset_class = TransFilter
    queryset = model.objects.filter()

@method_decorator(login_required, name='dispatch')
class LedgerList(ExportMixin, SingleTableMixin, FilterView):
    model = Transaction
    template_name = 'list_view.html'
    table_class = LedgerTable
    filterset_class = LedgerFilter
    queryset = model.objects.filter().order_by('-dt')
    # export_formats = (TableExport.XLS,)

@method_decorator(login_required, name='dispatch')
class AccountLogList(SingleTableView, FilterView):
    model = WalletHistory
    template_name = 'list_view.html'
    table_class = WalletHistoryTable

@method_decorator(staff_member_required, name="dispatch")
class AddChargesView(SuccessMessageMixin, CreateView):
    model = Charges
    template_name = 'form_view.html'
    fields = '__all__'
    success_message = 'Charge added successfully'
    success_url = reverse_lazy('trans:list_charges')

@method_decorator(staff_member_required, name="dispatch")
class ListChargesView(SingleTableView):
    model = Charges
    template_name = 'list_view.html'
    queryset = model.objects.filter()
    table_class = ChargesTable

@method_decorator(staff_member_required, name="dispatch")
class UpdateChargesView(SuccessMessageMixin, UpdateView):
    model = Charges
    template_name = 'form_view.html'
    success_message = 'Charge updated successfully'
    success_url = reverse_lazy('trans:list_charges')
    fields = "__all__"


@method_decorator(login_required, name="dispatch")
@method_decorator(UserDecorator, name="dispatch")
class AddPaymentRequestView(SuccessMessageMixin, CreateView):
    model = PaymentRequest
    template_name = 'form_view.html'
    form_class = RequestForm
    success_message = 'Payment Request Created successfully'
    success_url = reverse_lazy('trans:list_request')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name="dispatch")
@method_decorator(UserDecorator, name="dispatch")
class ListPaymentRequestView(SingleTableView):
    model = PaymentRequest
    template_name = 'list_view.html'
    queryset = model.objects.filter()
    table_class = PaymentRequestTable

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@method_decorator(staff_member_required, name="dispatch")
class UpdatePaymentRequestView(SuccessMessageMixin, UpdateView):
    model = PaymentRequest
    template_name = 'form_view.html'
    success_message = 'Payment Request Updated successfully'
    success_url = reverse_lazy('trans:list_request')
    fields = "__all__"
    queryset = model.objects.filter(status=1)

@method_decorator(staff_member_required, name="dispatch")
class AllPaymentRequestView(SingleTableView):
    model = PaymentRequest
    template_name = 'list_view.html'
    queryset = model.objects.filter()
    table_class = AllRequestTable


@method_decorator(staff_member_required, name="dispatch")
class AddBankView(SuccessMessageMixin, CreateView):
    model = Bank
    template_name = 'form_view.html'
    fields = '__all__'
    success_message = 'Bank Created successfully'
    success_url = reverse_lazy('trans:list_Bank')

@method_decorator(staff_member_required, name="dispatch")
class ListBankView(SingleTableView):
    model = Bank
    template_name = 'list_view.html'
    queryset = model.objects.filter()
    table_class = BankTable

@method_decorator(staff_member_required, name="dispatch")
class UpdateBankView(SuccessMessageMixin, UpdateView):
    model = Bank
    template_name = 'form_view.html'
    success_message = 'Bank Updated successfully'
    success_url = reverse_lazy('trans:list_Bank')
    fields = "__all__"
