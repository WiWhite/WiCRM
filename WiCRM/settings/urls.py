from django.urls import path
from .views import *

urlpatterns = [
    path('staff/', SettingsStaff.as_view(), name='settings_staff'),
    path('positions/', SettingsPositions.as_view(),
         name='settings_positions'),
    path('service/', SettingsService.as_view(),
         name='settings_services'),
    path('email-service/', SettingsEmailService.as_view(),
         name='settings_email_service'),
]
