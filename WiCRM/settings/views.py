from django.shortcuts import render, redirect
from django.views.generic import CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail, get_connection

from .models import *
from .forms import *
from .mixins import CreateDelObjectMixin
from .utils import *
from referral.models import Referrals


class SettingsStaff(LoginRequiredMixin, CreateView):
    """
    View for displaying, creating, updating and deleting employees.
    """
    model = Staff
    form_class = StaffForm
    template_name = 'settings/settings_staff.html'
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
            messages.success(
                self.request,
                f'{form.cleaned_data["first_name"]} '
                f'{form.cleaned_data["last_name"]} successfully created!'
            )
            form.save()

            staff = Staff.objects.get(email=form.cleaned_data['email'])
            service = EmailService.objects.get(pk=owner.pk)
            ref = Referrals.objects.get(pk=staff.referral_id)

            connection = create_connection(service)
            msg = f'{settings.ALLOWED_HOSTS[0]}:8000/registration-referral' \
                  f'={ref.referral_code}'
            send_invite(
                service.email_login,
                [form.cleaned_data['email']],
                connection,
                msg,
            )
            return redirect(self.request.path)
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
    template_name = 'settings/settings_positions.html'
    success_url = reverse_lazy('settings_positions')
    raise_exception = True


class SettingsService(LoginRequiredMixin, CreateDelObjectMixin):
    """
    View to display, create and delete the services provided.
    """
    model = Services
    form_class = ServicesForm
    template_name = 'settings/settings_services.html'
    success_url = reverse_lazy('settings_services')
    raise_exception = True


class SettingsEmailService(View):

    def get(self, request):

        try:
            obj = EmailService.objects.get(owner=request.user)
            form = EmailServiceForm(instance=obj)
            context = {
                'form': form,
                'obj': obj,
            }
            return render(
                request,
                'settings/settings_email_service.html',
                context
            )

        except models.ObjectDoesNotExist:
            form = EmailServiceForm()
            context = {
                'form': form,
            }
            return render(
                request,
                'settings/settings_email_service.html',
                context
            )

    def post(self, request):

        data = self.request.POST.copy()
        data['owner'] = self.request.user

        if self.request.POST.get('update'):
            obj = EmailService.objects.get(owner=request.user)
            form = EmailServiceForm(data, instance=obj)
            if form.is_valid():
                try:
                    check_connection(form.cleaned_data)
                    form.save()
                    messages.success(request, 'Successfully updated!')
                    return redirect(self.request.path)
                except:
                    messages.error(
                        request,
                        'Ooops! Your configure is incorrect!'
                    )
                    return redirect(self.request.path)

            else:
                messages.error(request, f'{form.errors}')
                return render(
                    request,
                    'settings/settings_email_service.html',
                    {'form': form}
                )

        form = EmailServiceForm(data)
        if form.is_valid():
            try:
                check_connection(form.cleaned_data)
                form.save()
                messages.success(request, 'Successfully created!')
                return redirect(self.request.path)
            except:
                messages.error(
                    request,
                    'Ooops! Your configure is incorrect!'
                )
                return redirect(self.request.path)

        else:
            messages.error(request, f'{form.errors}')
            return render(
                request,
                'settings/settings_email_service.html',
                {'form': form}
            )
