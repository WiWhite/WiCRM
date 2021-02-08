from datetime import datetime

from django import forms
from .models import *


class CustomerForm(forms.ModelForm):
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
                    'class': 'form-control form-control-sm'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'company': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'instagram': forms.URLInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'service': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
                }
            ),
            'curator': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
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
                    'class': 'form-control form-control-sm'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
            'phone_number': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
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
            'dismissal': forms.DateInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            )
        }


class PositionsForm(forms.ModelForm):
    class Meta:
        model = Positions
        fields = (
            'position_name',
        )

        widgets = {
            'position_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
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
        )

        widgets = {
            'service_name': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm'
                }
            ),
        }
