from smtplib import SMTPException

from django.views.generic import CreateView, View
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

from .utils import check_connection


class CreateDelObjectMixin(CreateView):
    model = None
    form_class = None
    template_name = None
    success_url = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['objects'] = self.model.objects.filter(owner=self.request.user)
        context['fields'] = self.model._meta.fields
        return context

    def delete(self, delete_pk):

        obj = self.model.objects.get(pk=delete_pk)
        obj.delete()
        messages.success(self.request, f'{obj} successfully deleted!')

    def post(self, request, *args, **kwargs):

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            self.delete(delete_pk)
            return redirect(self.request.path)

        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()
        self.request.POST['owner'] = f'{owner.pk}'
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class CheckConnSaveMixin(View):

    @staticmethod
    def check_save(request, form):

        try:
            check_connection(form.cleaned_data)
            form.save()
            messages.success(request, 'Successfully created!')

        except SMTPException:
            messages.error(
                request,
                'Ooops! Your configure is incorrect. Check the '
                'correctness of the data and try again.'
            )

        except TimeoutError:
            messages.error(
                request,
                'An attempt to establish a connection was unsuccessful'
                ' because the desired response was not received from'
                ' another computer within the required time, or an '
                'already established connection was terminated due to '
                'a bad response from an already connected computer.'
            )
