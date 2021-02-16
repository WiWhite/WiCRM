from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DeleteView
from django.contrib.auth.models import User
from .models import *
from .forms import *


class CustomersList(ListView):
    model = Customers
    template_name = 'customers/customers_list.html'
    extra_context = {
        'form': CustomerForm()
    }
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

    def post(self, request, *args, **kwargs):

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            customer = self.model.objects.get(pk=delete_pk)
            customer.delete()
            return redirect('customers_list')

        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            customer = self.model.objects.get(pk=update_pk)
            self.request.POST = self.request.POST.copy()
            self.request.POST['owner'] = self.request.user
            form = CustomerForm(self.request.POST, instance=customer)
            if form.is_valid():
                form.save()
                return redirect('customers_list')


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


class DetailCustomer(CreateView):
    model = Customers
    form_class = OrderForm
    template_name = 'customers/detail_customer.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        customer = self.request.path.split('/')[-1]
        context['orders'] = Orders.objects.filter(customer=customer)
        context['object'] = Customers.objects.get(pk=customer)
        context['fields'] = Orders._meta.fields

        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            order = Orders.objects.get(pk=delete_pk)
            order.delete()
            return redirect(self.request.path)

        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            order = Orders.objects.get(pk=update_pk)
            self.request.POST = self.request.POST.copy()
            self.request.POST['customer'] = self.object.id
            form = OrderForm(self.request.POST, instance=order)
            if form.is_valid():
                form.save()
                return redirect(self.request.path)

        context = self.get_context_data(**kwargs)
        self.request.POST = self.request.POST.copy()
        self.request.POST['customer'] = self.object.id
        form = self.form_class(self.request.POST)

        if form.is_valid():
            form.save()
            context['form'] = self.form_class()
            return render(self.request, self.template_name, context)
        else:
            return render(self.request, self.template_name, context)


class SettingsStaff(CreateView):
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

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            staff = self.model.objects.get(pk=delete_pk)
            staff.delete()
            return redirect('settings_staff')

        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            staff = self.model.objects.get(pk=update_pk)
            form = self.form_class(self.request.POST, instance=staff)
            if form.is_valid():
                form.save()
                return redirect('settings_staff')

        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form




        )


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

    def post(self, request, *args, **kwargs):

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            staff = self.model.objects.get(pk=delete_pk)
            staff.delete()
            return redirect('settings_positions')

        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


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

    def post(self, request, *args, **kwargs):

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            staff = self.model.objects.get(pk=delete_pk)
            staff.delete()
            return redirect('settings_services')

        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

