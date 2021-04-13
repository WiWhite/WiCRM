from django.db import models
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from settings.models import Services, Personnel


class Customers(models.Model):

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    company = models.CharField(max_length=50)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=40)
    instagram = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    curator = models.ForeignKey(Personnel, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Customers'
        verbose_name = 'Customer'


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

