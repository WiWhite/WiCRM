from django.views.generic import CreateView, ListView
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


class ObjListUpdateDeleteMixin(ListView):
    name_url = None
    form_class = None

    def get_queryset(self):

        # customer card search request
        search = self.request.GET.get('search', '')

        if search:
            # filtering customers by last_name and owner
            object_list = self.model.objects.filter(
                last_name=search.capitalize(),
                owner=self.request.user
            ).select_related()
            return object_list

        # filtering customers by owner
        object_list = self.model.objects.filter(
            owner=self.request.user
        ).select_related()
        return object_list

    def delete(self, delete_pk):

        customer = self.model.objects.get(pk=delete_pk)
        customer.delete()

    def update(self, update_pk):

        customer = self.model.objects.get(pk=update_pk)
        self.request.POST = self.request.POST.copy()  # a copy of POST is created because this object is immutable
        self.request.POST['owner'] = self.request.user  # add customer owner
        form = self.form_class(self.request.POST, instance=customer)
        if form.is_valid():
            form.save()

    def post(self, request, *args, **kwargs):

        # customer card delete request
        delete_pk = self.request.POST.get('delete_pk')
        if delete_pk:
            self.delete(delete_pk)
            return redirect(self.name_url)

        # customer card update request
        update_pk = self.request.POST.get('update_pk')
        if update_pk:
            self.update(update_pk)
            return redirect(self.name_url)