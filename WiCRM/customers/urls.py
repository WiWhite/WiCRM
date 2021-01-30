from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomersList.as_view(), name='customers_list'),
    path('create-customer/', CreateCustomer.as_view(), name='create_customer'),
]
