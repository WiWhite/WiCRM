from django.contrib import admin
from django.urls import path
from .views import RegistrationReferral

urlpatterns = [
    path('', RegistrationReferral.as_view(), name='registration_referral'),
]
