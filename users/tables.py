from django.utils.safestring import mark_safe
from django.utils.html import escape

import django_tables2 as tables
import django_filters

from django.contrib.auth import get_user_model
User = get_user_model()

class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    is_reseller = django_filters.ChoiceFilter(choices=[(True, 'Reseller'), (False, 'Retailer')])
    is_active = django_filters.ChoiceFilter(choices=[(True, 'Active'), (False, 'Inactive')])
    verify = django_filters.ChoiceFilter(choices=[(True, 'Verified'), (False, 'Unverified')], method='verify_filter')
    class Meta:
        model = User
        fields = ['is_reseller', 'email', 'is_active']

    def verify_filter(self, queryset, name, value):
        return queryset.filter(profile__verify=value)

class RetailerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.ChoiceFilter(choices=[(True, 'Active'), (False, 'Inactive')])
    verify = django_filters.ChoiceFilter(choices=[(True, 'Verified'), (False, 'Unverified')], method='verify_filter')
    profile__phone = django_filters.CharFilter(lookup_expr='icontains', label='Phone')

    class Meta:
        model = User
        fields = ['name', 'email', 'profile__phone', 'is_active']

    def verify_filter(self, queryset, name, value):
        return queryset.filter(profile__verify=value)

class UsersTable(tables.Table):
    name = tables.Column(orderable=False)
    username = tables.Column(orderable=False)
    email = tables.Column(orderable=False)
    profile__phone = tables.Column(orderable=False)
    get_update_url = tables.Column(orderable=False, verbose_name='Update')
    is_reseller = tables.Column(verbose_name='User Type')
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = ("name", 'username', 'email', 'is_active', 'is_reseller', 'profile__bal', 'profile__phone', 'profile__verify', 'date_joined', 'get_update_url')

    def render_get_update_url(self, value):
        return mark_safe('<a href="%s"><span class="fa fa-pencil-alt"></span></a>' % escape(value))

    def render_is_reseller(self, value):
        return 'Reseller' if value else 'Retailer'