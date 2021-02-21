from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DeleteView
from django.contrib.auth.models import User
from .models import *
from .forms import *

from .mixins import *


class CustomersList(ListView):
    """
    View is responsible for displaying the customer card.
    """
    model = Customers
    template_name = 'customers/customers_list.html'
    extra_context = {
        'form': CustomerForm()
    }
    paginate_by = 12

    def get_queryset(self):

        # customer card search request
        search = self.request.GET.get('search', '')

        if search:
            # filtering customers by company and owner
            object_list = Customers.objects.filter(
                company=search,
                owner=self.request.user
            ).select_related()
            return object_list

        # filtering customers by owner
        object_list = Customers.objects.filter(
            owner=self.request.user
        ).select_related()
        return object_list

    def post(self, request, *args, **kwargs):

        # customer card delete request
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            customer = self.model.objects.get(pk=delete_pk)
            customer.delete()
            return redirect(self.request.path)

        # customer card update request
        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            customer = self.model.objects.get(pk=update_pk)
            self.request.POST = self.request.POST.copy()  # a copy of POST is created because this object is immutable
            self.request.POST['owner'] = self.request.user  # add customer owner
            form = CustomerForm(self.request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('customers_list')


class CreateCustomer(CreateView):
    """
    View is responsible for displaying the client creation form and processing
    the POST request.
    """
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/create_customer.html'
    success_url = reverse_lazy('customers_list')

    def post(self, request, *args, **kwargs):
        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()   # a copy of POST is created because this object is immutable
        self.request.POST['owner'] = f'{owner.pk}'  # add customer owner.id
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DetailCustomer(CreateView):
    """
    The view is responsible for displaying the details of the client card.
    Form for creating sales orders and displaying order history.
    Processing order creation, updating and deletion.
    """
    model = Customers
    form_class = OrderForm
    template_name = 'customers/detail_customer.html'

    def get_context_data(self, **kwargs):

        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context['orders'] = Orders.objects.filter(customer=self.object.id)
        context['fields'] = Orders._meta.fields

        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        # order delete request
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            order = Orders.objects.get(pk=delete_pk)
            order.delete()
            return redirect(self.request.path)

        # order update request
        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            order = Orders.objects.get(pk=update_pk)
            self.request.POST = self.request.POST.copy()
            self.request.POST['customer'] = order.customer_id
            form = OrderForm(self.request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect(self.request.path)

        self.request.POST = self.request.POST.copy()
        self.request.POST['customer'] = self.object.id
        form = self.form_class(self.request.POST)

        if form.is_valid():
            form.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'detail_customer',
            args=(self.request.path.split('/')[-1])
        )


class SettingsStaff(CreateView):
    """
    View for displaying, creating, updating and deleting employees.
    """
    model = Staff
    form_class = StaffForm
    template_name = 'customers/settings_staff.html'
    success_url = reverse_lazy('settings_staff')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['staff'] = Staff.objects.filter(
            owner=self.request.user,
            dismissal=None
        )
        context['fields'] = Staff._meta.fields

        return context

    def post(self, request, *args, **kwargs):

        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()
        self.request.POST['owner'] = f'{owner.pk}'

        # staff delete request
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            staff = self.model.objects.get(pk=delete_pk)
            staff.delete()
            return redirect('settings_staff')

        # staff delete request
        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            staff = self.model.objects.get(pk=update_pk)
            form = self.form_class(self.request.POST, instance=staff)
            if form.is_valid():
                form.save()
                return redirect('settings_staff')

        # staff created
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SettingsPositions(CreateDelObjectMixin):
    """
    View to display, create and delete positions of my employees.
    """
    model = Positions
    form_class = PositionsForm
    template_name = 'customers/settings_positions.html'
    success_url = reverse_lazy('settings_positions')


class SettingsService(CreateDelObjectMixin):
    """
    View to display, create and delete the services provided.
    """
    model = Services
    form_class = ServicesForm
    template_name = 'customers/settings_services.html'
    success_url = reverse_lazy('settings_services')

