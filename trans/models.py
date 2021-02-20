from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth import get_user_model
User = get_user_model()

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