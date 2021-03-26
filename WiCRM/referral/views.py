from django.shortcuts import render
from django.views.generic import View
from django.db import models
from .models import Referrals


class RegistrationReferral(View):

    def get(self, request, ref):
        try:
            referral = Referrals.objects.get(referral_code=ref)
            if referral.used is True:
                return render(request, 'referral/registration_referral.html', {'ref': ref})
            else:
                return render(request, 'referral/registration_referral.html',
                              {})
        except models.ObjectDoesNotExist:
            return render(request, 'referral/registration_referral.html', {})
