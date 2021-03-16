from datetime import datetime

from django import forms
from .models import *

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


class CustomerForm(forms.ModelForm):

    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Phone Number'
            }
        )
    )

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

    def __init__(self, owner=None, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['curator'].queryset = Staff.objects.filter(
            owner=owner,
            dismissal=None,
        )


class StaffForm(forms.ModelForm):

    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Phone number'
            }
        )
    )

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
            'birthdate': forms.DateInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'id': 'datepicker',
                    'width': '240',
                    'readonly': 'readonly'
                }
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
                    'class': 'form-control form-control-sm',
                    'id': 'datepicker1',
                    'width': '385',
                    'readonly': 'readonly'
                },
            )
        }

    def __init__(self, owner=None, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)
        self.fields['position'].queryset = Positions.objects.filter(owner=owner)


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
            'customer',
            'deadline',
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
            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'id': 'datepicker',
                    'width': '365',
                    'readonly': 'readonly'
                },
            ),
        }

    def __init__(self, owner=None, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['service'].queryset = Services.objects.filter(owner=owner)


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


class OrderHistoryForm(forms.ModelForm):
    class Meta:
        model = OrderHistory
        fields = (
            'correction',
            'status',
            'deadline',
            'description',
            'order',
        )

        widgets = {
            'correction': forms.TextInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Correction'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'Description'
                }
            ),
            'status': forms.Select(
                attrs={
                    'class': 'form-select form-select-sm'
                }
            ),
            'deadline': forms.DateInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'id': 'datepicker',
                    'width': '260',
                    'readonly': 'readonly'
                },
            ),
        }
