from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DeleteView
from django.contrib.auth.models import User
from .models import *
from .forms import *

from .mixins import *
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class Logout(View):

    def get(self, request):
        logout(request)
        messages.success(request, 'Success Logout!')
        return redirect('login')


class CustomersList(LoginRequiredMixin, ObjListUpdateDeleteMixin):
    """
    View is responsible for displaying the customer card.
    """
    model = Customers
    template_name = 'customers/customers_list.html'
    paginate_by = 12
    name_url = 'customers_list'
    form_class = CustomerForm
    raise_exception = True


class CreateCustomer(CreateView, LoginRequiredMixin):
    """
    View is responsible for displaying the client creation form and processing
    the POST request.
    """
    model = Customers
    form_class = CustomerForm
    template_name = 'customers/create_customer.html'
    success_url = reverse_lazy('customers_list')
    raise_exception = True

    def get(self, requests, *args, **kwargs):
        owner = User.objects.get(username=self.request.user)
        form = self.form_class(owner=owner)
        return render(requests, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):

        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()   # a copy of POST is created because this object is immutable
        self.request.POST['owner'] = f'{owner.pk}'  # add customer owner.id
        self.object = owner.pk
        form = self.form_class(owner.pk, self.request.POST)
        if form.is_valid():
            messages.success(
                self.request,
                f'{form.cleaned_data["first_name"]} '
                f'{form.cleaned_data["last_name"]} successfully created!'
            )
            return self.form_valid(form)
        else:
            messages.error(
                self.request,
                f'{form.errors}'
            )
            return self.form_invalid(form)


class DetailCustomer(LoginRequiredMixin, CreateView):
    """
    The view is responsible for displaying the details of the client card.
    Form for creating sales orders and displaying order history.
    Processing order creation, updating and deletion.
    """
    model = Customers
    form_class = OrderForm
    template_name = 'customers/detail_customer.html'
    raise_exception = True

    def get(self, request, *args, **kwargs):

        owner = User.objects.get(username=self.request.user)

        self.object = self.get_object()
        form = self.form_class(owner.pk)

        context = super().get_context_data(**kwargs)
        context['orders'] = Orders.objects.filter(customer=self.object.id)
        context['fields'] = Orders._meta.fields
        context['form'] = form

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()
        owner = User.objects.get(username=self.request.user)

        # order delete request
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            order = Orders.objects.get(pk=delete_pk)
            order.delete()
            messages.success(self.request, 'Order successfully deleted!')
            return redirect(self.request.path)

        # order update request
        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            order = Orders.objects.get(pk=update_pk)
            self.request.POST = self.request.POST.copy()
            self.request.POST['customer'] = order.customer_id
            self.request.POST['deadline'] = order.deadline
            form = self.form_class(owner.pk, self.request.POST, instance=order)
            if form.is_valid():
                form.save()
                messages.success(self.request, 'Order successfully updated!')
                return redirect(self.request.path)

        self.request.POST = self.request.POST.copy()
        self.request.POST['customer'] = self.object.id
        form = self.form_class(owner.pk, self.request.POST)

        if form.is_valid():
            messages.success(self.request, 'Order successfully created!')
            return self.form_valid(form)
        else:
            messages.error(self.request, f'{form.errors}')
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'detail_customer',
            args=(self.request.path.split('/')[-1])
        )


class SettingsStaff(LoginRequiredMixin, CreateView):
    """
    View for displaying, creating, updating and deleting employees.
    """
    model = Staff
    form_class = StaffForm
    template_name = 'customers/settings_staff.html'
    success_url = reverse_lazy('settings_staff')
    raise_exception = True

    def get(self, requests, *args, **kwargs):
        owner = User.objects.get(username=self.request.user)
        self.object = owner
        form = self.form_class(owner=owner)
        context = super().get_context_data(**kwargs)
        context['staff'] = Staff.objects.filter(
            owner=self.request.user,
            dismissal=None
        )
        context['fields'] = Staff._meta.fields
        context['form'] = form
        return render(requests, self.template_name, context)

    def post(self, request, *args, **kwargs):

        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()
        self.request.POST['owner'] = f'{owner.pk}'

        # staff delete request
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            staff = self.model.objects.get(pk=delete_pk)
            staff.delete()
            messages.success(self.request, f'{staff} successfully deleted!')
            return redirect('settings_staff')

        # staff delete request
        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            staff = self.model.objects.get(pk=update_pk)
            form = self.form_class(owner.pk, self.request.POST, instance=staff)
            if form.is_valid():
                form.save()
                messages.success(
                    self.request,
                    f'{staff} successfully updated!'
                )
                return redirect('settings_staff')
            else:
                messages.error(
                    self.request,
                    f'{staff} has\'t been changed. The data isn\'t correct!'
                )
                return redirect('settings_staff')

        # staff created
        form = self.form_class(owner.pk, self.request.POST)
        self.object = owner
        if form.is_valid():
            messages.success(
                self.request,
                f'{form.cleaned_data["first_name"]} '
                f'{form.cleaned_data["last_name"]} successfully created!'
            )
            return self.form_valid(form)
        else:
            messages.error(
                self.request,
                f'{form.errors}'
            )
            return self.form_invalid(form)


class SettingsPositions(LoginRequiredMixin, CreateDelObjectMixin):
    """
    View to display, create and delete positions of my employees.
    """
    model = Positions
    form_class = PositionsForm
    template_name = 'customers/settings_positions.html'
    success_url = reverse_lazy('settings_positions')
    raise_exception = True


class SettingsService(LoginRequiredMixin, CreateDelObjectMixin):
    """
    View to display, create and delete the services provided.
    """
    model = Services
    form_class = ServicesForm
    template_name = 'customers/settings_services.html'
    success_url = reverse_lazy('settings_services')
    raise_exception = True


class OrderHistory(LoginRequiredMixin, CreateView):
    model = OrderHistory
    template_name = 'customers/history_order.html'
    form_class = OrderHistoryForm
    raise_exception = True

    def get(self, request, *args, **kwargs):

        self.object = None
        pk = self.request.path.split('/')[-1]

        context = super().get_context_data(**kwargs)
        context['corrections'] = self.model.objects.filter(
            order_id=pk
        )
        context['fields'] = self.model._meta.fields
        context['form'] = self.form_class()
        context['pk'] = pk

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        self.object = None
        pk = self.request.path.split('/')[-1]
        order = Orders.objects.get(pk=pk)

        self.request.POST = self.request.POST.copy()
        self.request.POST['order'] = order.id
        form = self.form_class(self.request.POST)

        if form.is_valid():
            messages.success(self.request, 'Edit successfully created!')
            return self.form_valid(form)
        else:
            messages.error(self.request, f'{form.errors}')
            return self.form_invalid(form)

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'history_order',
            args=(self.request.path.split('/')[-1])
        )

