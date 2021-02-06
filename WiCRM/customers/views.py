from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
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


class CreateOrder(CreateView):
    model = Orders
    form_class = OrderForm
    template_name = 'customers/create_order.html'
    success_url = reverse_lazy('detail_customer')


class DetailCustomer(DetailView):
    model = Customers
    template_name = 'customers/detail_customer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = Orders.objects.filter(customer=self.object.id)
        context['fields'] = Orders._meta.fields
        context['form'] = OrderForm
        return context


class SettingsStaff(CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'customers/settings_staff.html'
    success_url = reverse_lazy('settings_staff')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['staff'] = Staff.objects.filter(owner=self.request.user)
        context['fields'] = Staff._meta.fields
        return context

    def post(self, request, *args, **kwargs):
        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()
        self.request.POST['owner'] = f'{owner.pk}'
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SettingsPositions(CreateView):
    model = Positions
    form_class = PositionsForm
    template_name = 'customers/settings_positions.html'
    success_url = reverse_lazy('settings_positions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['positions'] = Positions.objects.all()
        context['fields'] = Positions._meta.fields
        return context


class SettingsService(CreateView):
    model = Services
    form_class = ServicesForm
    template_name = 'customers/settings_services.html'
    success_url = reverse_lazy('settings_services')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Services.objects.all()
        context['fields'] = Services._meta.fields
        return context
