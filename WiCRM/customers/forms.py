from datetime import datetime

from django import forms
from .models import *

from phonenumber_field.formfields import PhoneNumberField


class CustomerForm(forms.ModelForm):

    phone_number = PhoneNumberField(widget=forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Phone Number'
                }
            ))

    class Meta:
        model = Customers
        fields = (
            'first_name',
            'last_name',
            'company',
            'phone_number',
            'email',
            'instagram',
            'curator',
            'owner'
        )

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'First Name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Last Name'
                }
            ),
            'company': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Company'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'E-mail'
                }
            ),
            'instagram': forms.URLInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'URL Instagram'
                }
            ),
            'service': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm',
                    'placeholder': 'Service'
                }
            ),
            'curator': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm',
                }
            ),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'birthdate',
            'position',
            'sex',
            'dismissal',
            'owner'
        )

        widgets = {
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'First Name'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Last Name'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Phone Number'
                }
            ),
            'birthdate': forms.SelectDateWidget(
                attrs={'class': 'form-select form-select-sm mt-1'},
                years=range(1920, datetime.now().year + 1)
            ),
            'position': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
                }
            ),
            'sex': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
                }
            ),
            'dismissal': forms.SelectDateWidget(
                attrs={
                    'class': 'form-select form-select-sm mt-1',
                },
                years=range(datetime.now().year, datetime.now().year + 2)
            )
        }


class PositionsForm(forms.ModelForm):
    class Meta:
        model = Positions
        fields = (
            'position_name',
            'owner'
        )

        widgets = {
            'position_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Position'
                }
            ),
        }


class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = (
            'service',
            'price',
            'status',
            'customer'
        )

        widgets = {
            'service': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
                }
            ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
                }
            ),
        }


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = (
            'service_name',
            'owner'
        )

        widgets = {
            'service_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Service'
                }
            ),
        }
