from django import forms
from .models import *

from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget


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
            'email',
            'phone_number',
            'birthdate',
            'position',
            'sex',
            'dismissal',
            'owner',
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
            ),
            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control form-control-sm',
                    'placeholder': 'E-mail'
                }
            ),
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