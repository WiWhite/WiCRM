from django.urls import path
from .views import *

urlpatterns = [
    path('', CustomersList.as_view(), name='customers_list')
]
