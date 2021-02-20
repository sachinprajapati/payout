from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.utils.html import escape
from .tokens import account_activation_token

import django_tables2 as tables
from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView
import django_filters

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Profile
from .forms import RetailerForm, UserCreateForm

def Dashboard(request):
    return render(request, 'dashboard1.html', {})

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class AddUser(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    # fields = ("name", "username", "email", "is_active", "is_reseller")
    success_url = reverse_lazy('users:list_users')
    success_message = "%(name)s successfully created"

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

@method_decorator(staff_member_required(login_url=reverse_lazy('login')), name='dispatch')
class ListUsers(SingleTableMixin, FilterView):
    model = User
    table_class = UsersTable
    template_name = "users/list_view.html"
    queryset = model.objects.filter(is_staff=False, is_superuser=False)
    filterset_class = UserFilter


class RegisterRetailer(SuccessMessageMixin, CreateView):
    # model = Profile
    form_class = RetailerForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')
    success_message = 'User successfully created please check email and verify account'

class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, ('Your account have been confirmed.'))
            return redirect(reverse_lazy('login'))
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


class UpdateUsers(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = UserCreateForm
    template_name = 'users/user_form.html'