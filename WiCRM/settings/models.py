from django.db import models
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from referral.models import Referrals

from .utils import generate_ref_code


class Services(models.Model):

    service_name = models.CharField(max_length=50, verbose_name='Service name')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service_name}'

    class Meta:
        verbose_name_plural = 'Services'
        verbose_name = 'Service'


class Positions(models.Model):

    position_name = models.CharField(
        max_length=20,
        verbose_name='Position name'
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.position_name}'

    class Meta:
        verbose_name_plural = 'Positions'
        verbose_name = 'Position'


class Personnel(models.Model):

    SEX_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
    )
    first_name = models.CharField(max_length=20, verbose_name='First name')
    last_name = models.CharField(max_length=30, verbose_name='Last name')
    phone_number = PhoneNumberField(null=True, verbose_name='Phone number')
    birthdate = models.DateField(verbose_name='Birthdate')
    position = models.ForeignKey(
        Positions,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Position'
    )
    sex = models.SmallIntegerField(choices=SEX_CHOICES, verbose_name='Sex')
    hiring_date = models.DateField(
        auto_now_add=True,
        verbose_name='Hiring date'
    )
    dismissal = models.DateField(
        blank=True,
        null=True,
        verbose_name='Dismissal'
    )
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    referral = models.OneToOneField(Referrals, on_delete=models.CASCADE)
    email = models.EmailField(max_length=40, verbose_name='E-mail')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):

        if not self.referral_id:
            ref = Referrals(referral_code=generate_ref_code())
            ref.save()
            self.referral_id = ref.id
            super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Staff'
        verbose_name = 'Staff'


class EmailService(models.Model):

    email_host = models.CharField(max_length=20, verbose_name='E-mail host')
    email_port = models.IntegerField(verbose_name='E-mail port')
    email_login = models.EmailField(max_length=40, verbose_name='E-mail')
    email_password = models.CharField(max_length=20, verbose_name='E-mail password')
    email_use_ssl = models.BooleanField(default=False, verbose_name='Connection type - secured SSL')
    email_use_tls = models.BooleanField(default=False, verbose_name='Connection type - secured TLS')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
