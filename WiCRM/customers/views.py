from django.shortcuts import render
from django.views.generic import ListView
from .models import *


class CustomersList(ListView):
    model = Customers
    template_name = 'customers/customers_list.html'

    def get_queryset(self):
        object_list = Customers.objects.all().select_related()
        return object_list
