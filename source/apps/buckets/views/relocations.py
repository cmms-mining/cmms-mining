from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, DetailView, FormView

from apps.buckets.forms import BucketRelocationAttachmentForm, BucketRelocationForm
from apps.buckets.models import Bucket, BucketRelocation, BucketRelocationAttachment


class FormValidationMixin:
    def validate_form(self, form):
        new_relocation_date = self.relocation.date
        bucket = self.relocation.bucket

        if bucket.get_relocation():
            if new_relocation_date <= bucket.get_relocation().date:
                messages.warning(
                    self.request,
                    'Ошибка - дата перемещения не может быть меньше или равна дате предыдущего перемещения!',
                    )
                return False

            form.changed_data.remove('from_site')
            form.changed_data.remove('from_site_hidden')
            if not form.has_changed():
                messages.warning(self.request, 'Изменений не внесено!')
                return False

        if new_relocation_date > timezone.localtime().date():
            messages.warning(self.request, 'Ошибка - дата перемещения не может быть больше текущей даты!')
            return False

        return True


class BucketRelocationsTabView(DetailView):
    context_object_name = 'bucket'
    template_name = 'buckets/relocations/bucket_relocations_tab.html'

    def get_object(self):
        return get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['bucket_relocations_tab'] = True
        return context


class BucketRelocationCreateView(FormValidationMixin, CreateView):
    model = BucketRelocation
    form_class = BucketRelocationForm
    template_name = 'buckets/relocations/bucket_relocation_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        context['bucket_relocations_tab'] = True
        return context

    # Передаем объект Site в kwargs формы
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        if bucket.get_relocation():
            last_site_instance = bucket.get_relocation().to_site
            kwargs['site_instance'] = last_site_instance
        return kwargs

    def form_valid(self, form):
        relocation: BucketRelocation = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        relocation.bucket = bucket
        self.relocation = relocation
        if not self.validate_form(form):
            return redirect('bucket_relocations_tab', bucket_number=bucket.number)

        relocation.save()
        messages.success(self.request, 'Перемещение успешно добавлено!')
        return redirect('bucket_relocations_tab', bucket_number=bucket.number)


class BucketRelocationAttachmentCreateView(FormView):
    form_class = BucketRelocationAttachmentForm

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        relocation = get_object_or_404(BucketRelocation, pk=self.kwargs.get('relocation_pk'))

        attachment_form = self.get_form()
        attachment: BucketRelocationAttachment = attachment_form.save(commit=False)
        attachment.bucket_relocation = relocation
        attachment.save()

        return redirect('bucket_relocation_update', bucket_number=relocation.bucket.number, relocation_pk=relocation.pk)
