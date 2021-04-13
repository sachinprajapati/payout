from django.db import models
from django import forms
from django.core.validators import RegexValidator, MinValueValidator
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

User = get_user_model()
from datetime import date
from decimal import Decimal as dc
from users.models import WalletHistory

PAYMENT_MODE = [
    (1, 'IMPS'),
    (2, 'RTG')
]

SERVICE_TYPE = [
    (1, 'MoneyTransfer')
]

BOOLEAN_STATUS = [
    (0, 'Failure'),
    (1, 'Success'),
]

TRANS_TYPE = [
    (0, 'Debit'),
    (1, 'Credit')
]

class Bank(models.Model):
    name = models.CharField(max_length=255, verbose_name='Account Name')
    no = models.CharField(max_length=20, verbose_name='Account No')
    ifsc = models.CharField(max_length=11, validators=[RegexValidator(regex='^.{11}$', message='Length has to be 11', code='nomatch')], verbose_name='IFSC Code')
    branch = models.CharField(max_length=255, verbose_name='Branch Name')
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s' % self.name

    def get_update_url(self):
        return reverse_lazy('trans:update_Bank', kwargs={'pk': self.pk})

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message=_("Phone number must be entered 10 digits Long."))
    phone = models.CharField(validators=[phone_regex], max_length=10, null=True)
    bank_name = models.CharField(max_length=255)
    account_no = models.CharField(max_length=20)
    name = models.CharField(max_length=255, verbose_name=_("Beneficiary Name"))
    mode = models.PositiveIntegerField(choices=PAYMENT_MODE)
    ref_no = models.CharField(max_length=255, null=True ,verbose_name=_('Bank Ref No'))
    service = models.PositiveIntegerField(choices=SERVICE_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    debit_amt = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=_("Debit Amount"))
    status = models.PositiveIntegerField(choices=BOOLEAN_STATUS)
    type = models.PositiveIntegerField(choices=TRANS_TYPE)
    remarks = models.TextField(null=True)
    dt = models.DateTimeField(auto_now_add=True, verbose_name=_("Date & Time"))

# @receiver(post_save, sender=Transaction)
# def create_cart(sender, instance, created, **kwargs):
#     if created:
        # wh = WalletHistory(user=instance.user, prev_bal=)

CHARGE_TYPE = [
    (1, 'Fixed'),
    (2, 'Percent')
]

class Charges(models.Model):
    min_amount = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField()
    charges = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.PositiveIntegerField(choices=CHARGE_TYPE)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_charge = models.DecimalField(max_digits=10, decimal_places=2)
    dt = models.DateTimeField(auto_now_add=True)

    def get_update_url(self):
        return reverse_lazy('trans:update_charges', kwargs={'pk': self.pk})

def OnlyPast(value):
    today = date.today()
    if value > today:
        raise forms.ValidationError('Order Date cannot be in the future.')

REQUEST_STATUS = [
    (1, 'Pending'),
    (2, 'Confirm'),
    (3, 'Cancel'),
]

class PaymentRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(validators=[OnlyPast], verbose_name='Payment Date')
    amount = models.DecimalField(max_digits=10, decimal_places=0, validators=[MinValueValidator(dc(1000))], verbose_name='Request For Amount')
    type = models.PositiveSmallIntegerField(choices=PAYMENT_MODE, verbose_name='Payment Mode')
    deposit = models.ForeignKey(Bank, on_delete=models.CASCADE, verbose_name='Deposit Bank Name')
    ref = models.CharField(max_length=255, verbose_name='Bank Ref Number')
    remarks = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=REQUEST_STATUS, default=1)
    dt = models.DateTimeField(auto_now_add=True)

    def get_update_url(self):
        return reverse_lazy('trans:update_request', kwargs={'pk': self.pk})