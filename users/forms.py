from django import forms
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string

from .tokens import account_activation_token
from .models import Profile

from django.contrib.auth import get_user_model
User = get_user_model()

import random, string

class RetailerForm(forms.ModelForm):
    parent = forms.IntegerField(widget=forms.HiddenInput())
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea(attrs={'rows':'3'}))
    name = forms.CharField(max_length=125, label="Contact Person Name")
    class Meta:
        model = Profile
        exclude = ('bal', 'user', 'verify')

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('User already exists with this email')
        return self.cleaned_data['email']

    def save(self, commit=True):
        m = super(RetailerForm, self).save(commit=False)
        data = self.cleaned_data
        u = User(email=data['email'], name=data['name'], parent_id=data['parent'])
        # pwd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        pwd = 'admin123'
        u.set_password(pwd)
        u.save()
        if commit:
            m.user = u
            m.save()
            current_site = 'localhost:8000'
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': u,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                'token': account_activation_token.make_token(u),
                'pwd': pwd
            })
            u.email_user(subject, message)
        return m

class UserCreateForm(RetailerForm):
    is_reseller = forms.BooleanField(required=False)

    def clean_email(self):
        raise forms.ValidationError('Not Valid Email')

    def save(self, commit=True):
        m = super(RetailerForm, self).save(commit=False)
        data = self.cleaned_data
        print("data is", data)
        u = User(email=data['email'], name=data['name'], is_reseller=data['is_reseller'])
        pwd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        u.set_password(pwd)
        u.save()
        if commit:
            m.user = u
            m.save()
            current_site = 'localhost:8000'
            subject = 'Activate Your MySite Account'
            message = render_to_string('account_activation_email.html', {
                'user': u,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(u.pk)),
                'token': account_activation_token.make_token(u),
                'pwd': pwd
            })
            u.email_user(subject, message)
        return m

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': '3'}))
    name = forms.CharField(max_length=125, label="Contact Person Name")
    is_reseller = forms.BooleanField(required=False)

    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ('user', 'bal')

    def save(self, commit=True):
        m = super(UserUpdateForm, self).save(commit=False)
        data = self.cleaned_data
        m.user.name = data['name']
        m.user.is_reseller = self.cleaned_data['is_reseller']
        m.user.save()
        m.save()
        return m
