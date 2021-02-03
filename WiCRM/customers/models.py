from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


class Customers(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    phone_number = PhoneNumberField()
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

    service_name = models.CharField(max_length=50)

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
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    phone_number = PhoneNumberField(null=True)
    birthdate = models.DateField()
    position = models.ForeignKey(
        'Positions',
        on_delete=models.SET_NULL,
        null=True
    )
    sex = models.SmallIntegerField(choices=SEX_CHOICES)
    hiring_date = models.DateTimeField(auto_now_add=True)
    dismissal = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        verbose_name_plural = 'Staff'
        verbose_name = 'Staff'


class Positions(models.Model):

    position_name = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.position_name}'

    class Meta:
        verbose_name_plural = 'Positions'
        verbose_name = 'Position'


class Orders(models.Model):

    STATUS_CHOICES = (
        (0, 'Conversation'),
        (1, 'Signing'),
        (2, 'Pending'),
        (3, 'Done'),
    )
    customer = models.ForeignKey(
        Customers,
        on_delete=models.CASCADE,
        verbose_name='Customer'
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Cr')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Up')

    class Meta:
        verbose_name_plural = 'Orders'
        verbose_name = 'Order'
        ordering = ('-created_at',)

