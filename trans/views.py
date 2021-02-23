from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import PermissionRequiredMixin

from django_tables2.views import SingleTableMixin
from django_tables2 import SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.export import TableExport

from .models import Transaction
from .tables import TransFilter, DMTTable, LedgerTable, LedgerFilter
from django_filters.views import FilterView

class AddTrans(CreateView):
    model = Transaction
    fields = "__all__"
    template_name = "users/user_form.html"

# @method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class DMTReportList(ExportMixin, PermissionRequiredMixin, SingleTableMixin, FilterView):
    permission_required = 'trans.view_transaction'
    model = Transaction
    template_name = 'users/list_view.html'
    table_class = DMTTable
    filterset_class = TransFilter
    queryset = model.objects.filter().order_by('-dt')

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class LedgerList(ExportMixin, SingleTableMixin, FilterView):
    model = Transaction
    template_name = 'users/list_view.html'
    table_class = LedgerTable
    filterset_class = LedgerFilter
    queryset = model.objects.filter().order_by('-dt')
    # export_formats = (TableExport.XLS,)