from django.views.generic import View
from django.contrib.auth import login
from django.shortcuts import render, redirect

from .forms import LoginForm


class Login(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('customers_list')

        return render(request, 'login/login.html', {'form': form})
