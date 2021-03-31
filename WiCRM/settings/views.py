from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages

from .models import *
from .forms import *
from .mixins import CreateDelObjectMixin


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
        self.object = owner
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
        if form.is_valid():
            print(form.cleaned_data)
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
