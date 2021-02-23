from django.utils.safestring import mark_safe
from django.utils.html import escape

import django_tables2 as tables
import django_filters
from django_filters.widgets import RangeWidget, RangeWidget, forms

from .models import Transaction

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