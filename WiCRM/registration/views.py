from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib import messages

from .forms import RegisterForm



class Registration(View):

    def get(self, request):
        form = RegisterForm()
        return render(
            request,
            'registration/registration.html',
            {'form': form}
        )

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registration success!')
            return redirect('login')

        else:
            messages.error(request, 'Registration failed!')
            return render(
                request,
                'registration/registration.html',
                {'form': form}
            )
