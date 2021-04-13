from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import models
from django.contrib import messages

from .models import Referrals
from settings.forms import PersonnelForm
from registration.forms import RegisterForm
from settings.models import Personnel


class RegistrationReferral(View):

    def get(self, request, ref):
        try:
            referral = Referrals.objects.get(referral_code=ref)
            if referral.used is False:
                staff = Personnel.objects.get(referral_id=referral.id)
                staff_form = PersonnelForm(instance=staff)
                registration_form = RegisterForm({'email': staff.email})
                context = {
                    'staff_form': staff_form,
                    'registration_form': registration_form,
                }
                return render(
                    request,
                    'referral/registration_referral.html',
                    context
                )
            else:
                return render(
                    request,
                    'referral/registration_referral.html',
                    {}
                )
        except models.ObjectDoesNotExist:
            return render(request, 'referral/registration_referral.html', {})

    def post(self, request, ref):
        referral = Referrals.objects.get(referral_code=ref)
        staff = Personnel.objects.get(referral_id=referral.id)
        staff_data = {
            'first_name': self.request.POST.get('first_name'),
            'last_name': self.request.POST.get('last_name'),
            'email': self.request.POST.get('email'),
            'phone_number_0': self.request.POST.get('phone_number_0'),
            'phone_number_1': self.request.POST.get('phone_number_1'),
            'birthdate': self.request.POST.get('birthdate'),
            'position': staff.position,
            'sex': self.request.POST.get('sex'),
            'dismissal': staff.dismissal,
            'owner': staff.owner,
        }
        staff_form = PersonnelForm(staff.owner_id, staff_data, instance=staff)
        register_data = self.request.POST.copy()
        register_data['group'] = 1
        registration_form = RegisterForm(register_data)
        if all([staff_form.is_valid(), registration_form.is_valid()]):
            staff_form.save()
            registration_form.save()
            referral.used = True
            referral.save()
            messages.success(request, 'Registration success!')
            return redirect('login')
        else:
            messages.error(
                request,
                'Registration failed!'
            )
            context = {
                'staff_form': staff_form,
                'registration_form': registration_form,
            }
            return render(
                request,
                'referral/registration_referral.html',
                context
            )


