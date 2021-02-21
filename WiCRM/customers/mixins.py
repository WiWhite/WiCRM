from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.models import User


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

    def post(self, request, *args, **kwargs):

        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            obj = self.model.objects.get(pk=delete_pk)
            obj.delete()
            return redirect(self.request.path)

        owner = User.objects.get(username=self.request.user)
        self.request.POST = self.request.POST.copy()
        self.request.POST['owner'] = f'{owner.pk}'
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
