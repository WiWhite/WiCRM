from django.shortcuts import render
from django.views.generic import ListView
from .models import *


class CustomersList(ListView):
    model = Customers
    template_name = 'customers/customers_list.html'
    paginate_by = 12

    def get_queryset(self):
        search = self.request.GET.get('search', '')

        if search:
            object_list = Customers.objects.filter(
                company=search
            ).select_related()
            return object_list

        object_list = Customers.objects.all().select_related()
        return object_list
