from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from accounts.models import User
from settings.models import Personnel
from django.contrib import messages


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

        user = User.objects.get(username=self.request.user)
        if user.group == 0:
            # filtering customers by owner
            object_list = self.model.objects.filter(
                owner=self.request.user
            ).select_related()
            return object_list
        else:
            # filtering customers by curator
            staff = Personnel.objects.get(email=user.email)
            object_list = self.model.objects.filter(
                curator=staff.id
            ).select_related()
            return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = object_list if object_list is not None else self.object_list
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(
                queryset, page_size)
            context = {
                'paginator': paginator,
                'page_obj': page,
                'is_paginated': is_paginated,
                'object_list': queryset,
                'form': self.form_class(self.request.user),
            }
        else:
            context = {
                'paginator': None,
                'page_obj': None,
                'is_paginated': False,
                'object_list': queryset,
                'form': self.form_class(self.request.user),
            }
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super().get_context_data(**context)

    def delete(self, delete_pk):

        obj = self.model.objects.get(pk=delete_pk)
        obj.delete()
        messages.success(self.request, f'{obj} successfully deleted!')

    def update(self, update_pk):

        owner = User.objects.get(username=self.request.user)
        obj = self.model.objects.get(pk=update_pk)
        self.request.POST = self.request.POST.copy()  # a copy of POST is created because this object is immutable
        self.request.POST['owner'] = self.request.user  # add customer owner
        form = self.form_class(owner.pk, self.request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(self.request, f'{obj} successfully updated!')
        else:
            messages.error(
                self.request,
                f'{obj} has\'t been changed. The data isn\'t correct!'
            )

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