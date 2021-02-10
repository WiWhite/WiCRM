from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomersList.as_view(), name='customers_list'),
    path('create-customer/', CreateCustomer.as_view(), name='create_customer'),
    path('detail-customer/<int:pk>', DetailCustomer.as_view(),
         name='detail_customer'),
    path('settings-staff/', SettingsStaff.as_view(), name='settings_staff'),
    path('settings-positions/', SettingsPositions.as_view(),
         name='settings_positions'),
    path('settings-service/', SettingsService.as_view(),
         name='settings_services'),
    # path('delete-customer/<int:pk>', DeleteCustomer.as_view(),
    #      name='delete_customer')
]
