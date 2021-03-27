from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from referral.models import Referrals
from .utils import generate_ref_code


class Customers(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=30)
    instagram = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    curator = models.ForeignKey('Staff', on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Customers'
        verbose_name = 'Customer'


class Services(models.Model):

    service_name = models.CharField(max_length=50, verbose_name='Service name')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.service_name}'

    class Meta:
        verbose_name_plural = 'Services'
        verbose_name = 'Service'


class Staff(models.Model):

    SEX_CHOICES = (
        (0, 'Male'),
        (1, 'Female'),
    )
    first_name = models.CharField(max_length=20, verbose_name='First name')
    last_name = models.CharField(max_length=30, verbose_name='Last name')
    phone_number = PhoneNumberField(null=True, verbose_name='Phone number')
    birthdate = models.DateField(verbose_name='Birthdate')
    position = models.ForeignKey(
        'Positions',
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


class Orders(models.Model):

    STATUS_CHOICES = (
        (0, 'Briefing'),
        (1, 'Moodboard'),
        (2, 'Develop'),
        (3, 'Correction'),
        (4, 'Done'),
    )

    service = models.ForeignKey(
        Services,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Service'
    )
    price = models.DecimalField(
        max_digits=11,
        decimal_places=2,
        verbose_name='Price'
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        verbose_name='Status'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Start')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Up')
    customer = models.ForeignKey(
        Customers,
        on_delete=models.CASCADE,
        verbose_name='Customer'
    )
    deadline = models.DateField(
        blank=True,
        null=True,
        verbose_name='Deadline'
    )

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'
        ordering = ('-created_at',)


class OrderHistory(models.Model):

    STATUS_CHOICES = (
        (0, 'In process'),
        (1, 'Done'),
        (2, 'Approved'),
    )

    correction = models.CharField(max_length=100, verbose_name='Correction')
    description = models.TextField(verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Start')
    order = models.ForeignKey(
        Orders,
        on_delete=models.CASCADE,
        verbose_name='Order'
    )
    deadline = models.DateField(
        blank=True,
        null=True,
        verbose_name='Deadline'
    )
    status = models.SmallIntegerField(
        choices=STATUS_CHOICES,
        verbose_name='Status'
    )

    class Meta:
        verbose_name_plural = 'Orders histories'
        verbose_name = 'Order history'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.correction}'

