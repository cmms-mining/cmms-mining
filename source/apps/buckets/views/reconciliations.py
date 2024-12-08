from datetime import timedelta
from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, DetailView, TemplateView

from apps.buckets.forms import BucketReconciliationForm
from apps.buckets.models import Bucket, BucketReconciliation
from apps.buckets.settings import DAYS_TO_BUCKETS_RECONCILIATION


class BucketReconciliationsTabView(DetailView):
    context_object_name = 'bucket'
    template_name = 'buckets/reconciliations/bucket_reconciliations_tab.html'

    def get_object(self):
        return get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['reconciliations_tab'] = True

        if not self.get_object().get_reconciliation():
            return context

        last_reconciliation_date = self.get_object().get_reconciliation().date

        days_from_reconciliation = (timezone.localtime().date() - last_reconciliation_date).days

        days_to_reconciliation = DAYS_TO_BUCKETS_RECONCILIATION - days_from_reconciliation

        date_to_reconciliation = timezone.localtime().date() + timedelta(days=days_to_reconciliation)
        context['date_to_reconciliation'] = date_to_reconciliation
        return context


class BucketReconciliationCreateView(CreateView):
    model = BucketReconciliation
    form_class = BucketReconciliationForm
    template_name = 'buckets/reconciliations/bucket_reconciliation_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        context['reconciliations_tab'] = True
        return context

    def form_valid(self, form):
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))

        errors = {}

        location = form.cleaned_data.get('location')
        if bucket.get_relocation() and bucket.get_relocation().to_site != location:
            errors['location'] = location.name

        equipment = form.cleaned_data.get('equipment')
        if bucket.get_equipment() != equipment:
            if equipment:
                errors['equipment'] = equipment.number
            else:
                errors['equipment'] = 'не установлен'

        adapter = form.cleaned_data.get('adapter').name
        if not bucket.tooth_adapter or bucket.tooth_adapter.name != adapter:
            errors['adapter'] = adapter

        techstate = form.cleaned_data.get('techstate')
        if bucket.get_techstate().techstate != techstate:
            errors['techstate'] = techstate.name

        if form.cleaned_data.get('is_operable') == 'True':
            is_operable = True
        else:
            is_operable = False
        if bucket.get_is_operable() != is_operable:
            errors['is_operable'] = is_operable

        if form.cleaned_data.get('is_being_repaired') == 'True':
            is_being_repaired = True
        else:
            is_being_repaired = False
        if bucket.get_is_being_repaired() != is_being_repaired:
            errors['is_being_repaired'] = is_being_repaired

        if errors:
            self.request.session['errors'] = errors
            return redirect('bucket_reconciliation_invalid', bucket_number=bucket.number)

        reconciliation: BucketReconciliation = form.save(commit=False)
        reconciliation.bucket = bucket
        reconciliation.save()
        messages.success(self.request, 'Сверка по ковшу успешно пройдена!')
        bucket.requires_reconciliation = False
        bucket.save()
        return redirect('bucket_reconciliations_tab', bucket_number=bucket.number)

    # Передаем объект bucket в kwargs формы
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        kwargs['bucket'] = bucket
        return kwargs


class BucketReconciliationInvalidView(TemplateView):
    template_name = 'buckets/reconciliations/bucket_reconciliation_invalid.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        errors = self.request.session['errors']
        context['errors'] = errors
        return context
