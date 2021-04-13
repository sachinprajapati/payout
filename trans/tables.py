from django.utils.safestring import mark_safe
from django.utils.html import escape

import django_tables2 as tables
import django_filters
from django_filters.widgets import RangeWidget, RangeWidget, forms

from .models import *

class RangeWidgetCustom(RangeWidget):
    template_name = 'filter_form.html'

class TransFilter(django_filters.FilterSet):
    dt = django_filters.DateFromToRangeFilter(widget=RangeWidget(attrs={'placeholder': 'YYYY/MM/DD', 'type': 'date'}), label="Date Range")
    # dt__gte = django_filters.DateFilter(widget=forms.DateInput(attrs={'type':'date'}), label='From', lookup_expr='gte', field_name='dt')
    # dt__lte = django_filters.DateFilter(widget=forms.DateInput(attrs={'type':'date'}), label='To', lookup_expr='lte', field_name='dt')
    class Meta:
        model = Transaction
        fields = ['dt', 'mode', 'phone']

    def verify_filter(self, queryset, name, value):
        return queryset.filter(profile__verify=value)

class DMTTable(tables.Table):
    phone = tables.Column(orderable=False)
    bank_name = tables.Column(orderable=False)
    account_no = tables.Column(orderable=False)
    name = tables.Column(orderable=False)
    ref_no = tables.Column(orderable=False)
    class Meta:
        model = Transaction
        attrs = {"class": "table table-bordered table-hover dataTable dtr-inline table-sm"}
        fields = ('id', 'dt', 'phone', 'bank_name', 'account_no', 'name', 'mode', 'ref_no', 'service', 'amount', 'debit_amt', 'status')

    def render_status(self, value):
        return mark_safe('<span class="badge bg-success">%s</span>' % escape(value)) if value else mark_safe('<span class="badge bg-danger">%s</span>' % escape(value))

class LedgerFilter(TransFilter):
    class Meta:
        model = Transaction
        fields = ['dt', 'mode', 'type']


class LedgerTable(tables.Table):
    remarks = tables.Column(orderable=False)
    class Meta(DMTTable.Meta):
        fields = ('id', 'dt', 'amount', 'mode', 'type', 'status', 'remarks')

class WalletHistoryTable(tables.Table):
    class Meta:
        model = WalletHistory
        fields = ('prev_bal', 'amount', 'remarks', 'dt')

class ChargesTable(tables.Table):
    get_update_url = tables.Column(orderable=False)
    class Meta:
        model = Charges
        fields = ('min_amount', 'max_amount', 'charges', 'type', 'commission', 'minimum_charge', 'get_update_url')

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))


class BankTable(tables.Table):
    get_update_url = tables.Column(orderable=False, verbose_name='Edit')
    class Meta:
        model = Bank
        attrs = {"class": "table table-bordered table-hover dataTable dtr-inline table-sm"}
        fields = ('name', 'no', 'ifsc', 'branch', 'remarks', 'get_update_url')

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))


class PaymentRequestTable(tables.Table):
    get_type_display = tables.Column(orderable=False, verbose_name='Type')
    class Meta:
        model = PaymentRequest
        attrs = {"class": "table table-bordered table-hover dataTable dtr-inline table-sm"}
        fields = ('date', 'amount', 'get_type_display', 'deposit', 'ref', 'status', 'remarks')

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

class AllRequestTable(tables.Table):
    get_update_url = tables.Column(orderable=False, verbose_name='Edit')
    get_type_display = tables.Column(orderable=False, verbose_name='Type')
    class Meta:
        model = PaymentRequest
        attrs = {"class": "table table-bordered table-hover dataTable dtr-inline table-sm"}
        fields = ('date', 'amount', 'get_type_display', 'deposit', 'ref', 'remarks', 'status', 'get_update_url')

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))