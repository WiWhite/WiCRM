from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError

from accounts.models import User


class RegisterForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
            'group',
        )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Your first name'
        }),
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Your last name'
        }),
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Your username'
        }),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'example@domain.ua'
        }),
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Password'
        }),
        label='Password'

    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Confirm password'
        }),
        label='Password confirmation'
    )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
