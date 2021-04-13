from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views import View
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token

from django_tables2.views import SingleTableMixin
from django_filters.views import FilterView

from .tables import UserFilter, UsersTable, RetailerFilter

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Profile
from .forms import RetailerForm, UserCreateForm, UserUpdateForm

def UserDecorator(function):
    def wrapper(request, *args, **kw):
        user=request.user
        if not (user.is_reseller or user.is_staff):
            return HttpResponseRedirect(reverse_lazy('users:dashboard'))
        else:
            return function(request, *args, **kw)
    return wrapper

def Dashboard(request):
    print(request.user.is_retailler())
    return render(request, 'dashboard.html', {})

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
@method_decorator(UserDecorator, name='dispatch')
class AddUser(SuccessMessageMixin, CreateView):
    form_class = UserCreateForm
    template_name = 'users/user_form.html'
    # fields = ("name", "username", "email", "is_active", "is_reseller")
    success_url = reverse_lazy('users:list_users')
    success_message = "%(name)s successfully created"

    def get_initial(self):
        return {'parent': self.request.user.pk}

    def get_form_class(self):
        if self.request.user.is_reseller:
            return RetailerForm
        else:
            return self.form_class

    def form_valid(self, form):
        form.instance.parent = self.request.user
        return super(AddUser, self).form_valid(form)

@method_decorator(login_required(login_url=reverse_lazy('login')), name='dispatch')
@method_decorator(UserDecorator, name='dispatch')
class ListUsers(SingleTableMixin, FilterView):
    model = User
    table_class = UsersTable
    template_name = "users/list_view.html"
    queryset = model.objects.filter(is_staff=False, is_superuser=False).order_by('-date_joined')
    filterset_class = UserFilter

    def get_queryset(self):
        if self.request.user.is_reseller:
            return self.queryset.filter(parent=self.request.user)
        return self.queryset

    def get_filterset_class(self):
        if self.request.user.is_staff:
            return self.filterset_class
        else:
            return RetailerFilter


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
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
        return redirect(reverse_lazy('login'))

class UpdateUsers(SuccessMessageMixin, UpdateView):
    model = Profile
    form_class = UserUpdateForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:list_users')
    success_message = '%(email)s successfully updated'

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = self.get_object().user.email
        initial['name'] = self.get_object().user.name
        initial['is_reseller'] = self.get_object().user.is_reseller
        return initial