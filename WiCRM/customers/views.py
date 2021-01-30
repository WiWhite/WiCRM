from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import *
from .forms import *


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


class CreateCustomer(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/create_customer.html'
    success_url = reverse_lazy('customers_list')
