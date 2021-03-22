from django.views.generic import View
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import LoginForm


class Login(View):

    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('customers_list')
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            messages.success(
                request,
                f'Welcome {request.user}!'
            )
            return redirect('customers_list')
        messages.error(
            request,
            f'Login failed!'
        )
        return render(request, 'login/login.html', {'form': form})
