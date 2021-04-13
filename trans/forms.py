from django import forms
from datetime import date

from .models import *

from decimal import Decimal as dc

class RequestForm(forms.ModelForm):
    date = forms.CharField(widget=forms.TextInput(attrs={'type': 'date', 'max': date.today()}))
    class Meta:
        model = PaymentRequest
        exclude = ('user', 'dt')

    def save(self, commit=True):
        m = super(RequestForm, self).save(commit=False)
        if commit:
            m.user.profile.bal += dc(self.cleaned_data['amount'])
            m.save()
        return m
