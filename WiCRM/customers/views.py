from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View, DeleteView
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import *
from .forms import *
from .mixins import *
from accounts.models import User



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


class CreateCustomer(LoginRequiredMixin, CreateView):
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
        self.object = None
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
                messages.success(self.request, 'Order successfully updated!')
                return self.form_valid(form)
            else:
                messages.error(
                    self.request,
                    f'{order} has\'t been changed. The data isn\'t correct!'
                )
                return self.form_invalid(form)

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

        self.request.POST = self.request.POST.copy()
        self.request.POST['order'] = pk
        form = self.form_class(self.request.POST)

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            correction = self.model.objects.get(pk=delete_pk)
            correction.delete()
            messages.success(self.request, f'{correction} successfully deleted!')
            return redirect(self.request.path)

        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            correction = self.model.objects.get(pk=update_pk)
            self.request.POST['deadline'] = correction.deadline
            form = self.form_class(self.request.POST, instance=correction)
            if form.is_valid():
                messages.success(
                    self.request,
                    f'{correction} successfully updated!'
                )
                return self.form_valid(form)
            else:
                messages.error(
                    self.request,
                    f'{correction} has\'t been changed. The data isn\'t correct!'
                )
                return self.form_invalid(form)

        if form.is_valid():
            messages.success(
                self.request,
                f'{form.cleaned_data["correction"]} successfully created!'
            )
            return self.form_valid(form)
        else:
            messages.error(self.request, f'{form.errors}')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy(
            'history_order',
            args=(self.request.path.split('/')[-1])
        )

