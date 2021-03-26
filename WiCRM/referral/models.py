from django.db import models


class Referrals(models.Model):
    referral_code = models.CharField(max_length=40)
    used = models.BooleanField(default=False)

    def __str__(self):
        return self.referral_code
