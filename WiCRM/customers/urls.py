from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomersList.as_view(), name='customers_list'),
    path('create-customer/', CreateCustomer.as_view(), name='create_customer'),
    path('detail-customer/<int:pk>', DetailCustomer.as_view(),
         name='detail_customer'),
]
