from django.db import models

from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.core.validators import RegexValidator
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from decimal import Decimal as dc


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=55, unique=True, null=True, verbose_name=_('Bank Id'))
    name = models.CharField(max_length=125, blank=True)
    is_active = models.BooleanField(_('active'), default=False)
    is_reseller = models.BooleanField(_('Reseller'), default=False)
    is_staff = models.BooleanField(_('Staff'), default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children')
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    @property
    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def get_update_url(self):
        return reverse_lazy('users:update_user', kwargs={'pk': self.profile.pk})

    def is_retailler(self):
        if not self.is_reseller or not self.is_staff or not self.is_superuser:
            return False
        return True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    bal = models.DecimalField(max_digits=12, decimal_places=4, verbose_name=_("Wallet Balance"), default=0)
    company = models.CharField(max_length=255, verbose_name=_("Company Name"))
    address = models.TextField()
    pincode_regex = RegexValidator(regex=r'^\+?1?\d{6}$', message="Pincode must be entered 6 digits Long.")
    pincode = models.CharField(validators=[pincode_regex], max_length=6, null=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{10}$', message="Phone number must be entered 10 digits Long.")
    phone = models.CharField(validators=[phone_regex], max_length=10, null=True)  # validators should be a list
    pan_no = models.CharField(max_length=10, null=True)
    pan_name = models.CharField(max_length=125, verbose_name=_("as on Pan Card Name"))
    gst_no = models.CharField(max_length=15, null=True)
    verify = models.BooleanField(default=False)

    def __str__(self):
        return '{} {}'.format(self.user, self.bal)


class WalletHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    prev_bal = models.DecimalField(max_digits=12, decimal_places=4, verbose_name=_("Previous Balace"))
    amount = models.DecimalField(max_digits=10, decimal_places=4, verbose_name=_("Amount Added"))
    remarks = models.TextField(null=True)
    dt = models.DateTimeField(auto_now_add=True)

    unique_together = ['wallet', 'order']

