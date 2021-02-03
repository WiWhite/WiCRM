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
