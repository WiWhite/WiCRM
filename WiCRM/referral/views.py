from django.shortcuts import render
from django.views.generic import View
from django.db import models

from .models import Referrals
from customers.forms import StaffForm
from registration.forms import RegisterForm
from customers.models import Staff


class RegistrationReferral(View):

    def get(self, request, ref):
        try:
            referral = Referrals.objects.get(referral_code=ref)
            if referral.used is False:
                staff = Staff.objects.get(referral_id=referral.id)
                staff_form = StaffForm(instance=staff)
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
