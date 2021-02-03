from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.models import User
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
                company=search,
                owner=self.request.user
            ).select_related()
            return object_list

        object_list = Customers.objects.filter(
            owner=self.request.user
        ).select_related()
        return object_list


class CreateCustomer(CreateView):
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/create_customer.html'
    success_url = reverse_lazy('customers_list')

    def post(self, request, *args, **kwargs):
        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()
        self.request.POST['owner'] = f'{owner.pk}'
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
