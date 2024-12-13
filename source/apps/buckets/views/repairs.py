from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.buckets.forms import BucketRepairForm
from apps.buckets.models import Bucket, BucketRepair, BucketTechState
from apps.common.models import TechStateOption


class FormValidationMixin:
    def validate_form(self, form):
        bucket: Bucket = self.repair.bucket

        if isinstance(self, BucketRepairCreateView):
            if bucket.get_is_being_repaired() or bucket.is_awaiting_repair():
                messages.warning(
                    self.request,
                    'Ошибка - Вы не можете создать новый ремонт, пока не закончен предыдущий!',
                    )
                return False

            new_repair_plan_start_date = self.repair.plan_start_date
            if new_repair_plan_start_date and new_repair_plan_start_date < timezone.localtime().date():
                messages.warning(
                    self.request,
                    'Ошибка - дата планового начала ремонта не может быть меньше текущей даты!',
                    )
                return False

            new_repair_plan_end_date = self.repair.plan_end_date
            if new_repair_plan_end_date and new_repair_plan_end_date < timezone.localtime().date():
                messages.warning(
                    self.request,
                    'Ошибка - дата планового окончания ремонта не может быть меньше текущей даты!',
                    )
                return False

            if new_repair_plan_start_date and new_repair_plan_end_date and \
                    new_repair_plan_end_date < new_repair_plan_start_date:
                messages.warning(
                    self.request,
                    'Ошибка - дата планового окончания ремонта не может быть больше даты планового начала ремонта!',
                    )
                return False

        if isinstance(self, BucketRepairUpdateView):
            old_repair_plan_start_date = self.object.bucket.get_repair().plan_start_date
            new_repair_plan_start_date = self.repair.plan_start_date
            if new_repair_plan_start_date:
                if old_repair_plan_start_date:
                    if (old_repair_plan_start_date != new_repair_plan_start_date) and \
                            new_repair_plan_start_date < timezone.localtime().date():
                        messages.warning(
                            self.request,
                            'Ошибка - дата планового начала ремонта не может быть меньше текущей даты!',
                            )
                        return False
                elif new_repair_plan_start_date < timezone.localtime().date():
                    messages.warning(
                        self.request,
                        'Ошибка - дата планового начала ремонта не может быть меньше текущей даты!',
                        )
                    return False

            old_repair_plan_end_date = self.object.bucket.get_repair().plan_end_date
            new_repair_plan_end_date = self.repair.plan_end_date
            if new_repair_plan_end_date:
                if old_repair_plan_end_date:
                    if (old_repair_plan_end_date != new_repair_plan_end_date) and \
                            new_repair_plan_end_date < timezone.localtime().date():
                        messages.warning(
                            self.request,
                            'Ошибка - дата планового окончания ремонта не может быть меньше текущей даты!',
                            )
                        return False
                elif new_repair_plan_end_date < timezone.localtime().date():
                    messages.warning(
                        self.request,
                        'Ошибка - дата планового окончания ремонта не может быть меньше текущей даты!',
                        )
                    return False

            if form.cleaned_data.get('plan_start_date_hidden'):
                form.changed_data.remove('plan_start_date_hidden')
                form.changed_data.remove('plan_start_date')
            if form.cleaned_data.get('start_date_hidden'):
                form.changed_data.remove('start_date_hidden')
                form.changed_data.remove('start_date')
            if form.cleaned_data.get('plan_end_date_hidden'):
                form.changed_data.remove('plan_end_date_hidden')
                form.changed_data.remove('plan_end_date')
            if form.cleaned_data.get('end_date_hidden'):
                form.changed_data.remove('end_date_hidden')
                form.changed_data.remove('end_date')
            if not form.has_changed():
                messages.warning(self.request, 'Изменений не внесено!')
                return False

        new_repair_start_date = self.repair.start_date
        if new_repair_start_date and new_repair_start_date > timezone.localtime().date():
            messages.warning(self.request, 'Ошибка - дата начала ремонта не может быть больше текущей!')
            return False

        new_repair_end_date = self.repair.end_date
        if new_repair_end_date and new_repair_end_date > timezone.localtime().date():
            messages.warning(self.request, 'Ошибка - дата окончания ремонта не может быть больше текущей!')
            return False

        if new_repair_end_date and not new_repair_start_date:
            messages.warning(
                self.request, 'Ошибка - Вы не можете указать дату окончания ремонта без указания даты начала ремонта!',
                )
            return False

        # TODO оформить логику ошибки
        if False:
            messages.warning(
                self.request, 'Ошибка - дата начала ремонта не может быть меньше или равна '
                              'дате окончания предыдущего ремонта!',
                )
            return False

        return True


class BucketRepairsListView(TemplateView):
    """Список ремонтов ковша"""
    template_name = 'buckets/repairs/bucket_repairs_tab.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['bucket'] = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['repairs_tab'] = True
        return context


class BucketRepairCreateView(FormValidationMixin, CreateView):
    model = BucketRepair
    form_class = BucketRepairForm
    template_name = 'buckets/repairs/bucket_repair_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        context['repairs_tab'] = True
        return context

    def form_valid(self, form):
        repair = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        repair.bucket = bucket
        self.repair = repair
        if not self.validate_form(form):
            return redirect('bucket_repairs_tab', bucket_number=bucket.number)
        repair.save()
        if repair.end_date:
            techstate_status = get_object_or_404(TechStateOption, name='Ремонта не требует')
            BucketTechState.objects.create(
                bucket=bucket,
                date=repair.end_date,
                techstate=techstate_status,
                is_operable=True,
                author=self.request.user,
            )
            messages.success(self.request, 'Ремонт успешно завершен! Техсостояние обновлено!')
        else:
            messages.success(self.request, 'Ремонт успешно добавлен!')
        return redirect('bucket_repairs_tab', bucket_number=bucket.number)


class BucketRepairUpdateView(FormValidationMixin, UpdateView):
    form_class = BucketRepairForm
    context_object_name = 'repair'
    template_name = 'buckets/repairs/bucket_repair_update.html'

    def get_object(self):
        obj = get_object_or_404(BucketRepair, pk=self.kwargs.get('repair_pk'))
        self.old_end_date = obj.end_date
        return obj

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['bucket'] = self.object.bucket
        context['repairs_tab'] = True
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        if bucket.get_repair():
            kwargs['plan_start_date'] = bucket.get_repair().plan_start_date
            kwargs['plan_end_date'] = bucket.get_repair().plan_end_date
            kwargs['start_date'] = bucket.get_repair().start_date
            kwargs['end_date'] = bucket.get_repair().end_date
        return kwargs

    def form_valid(self, form):
        repair: BucketRepair = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        repair.bucket = bucket
        self.repair = repair
        if not self.validate_form(form):
            return redirect('bucket_repairs_tab', bucket_number=bucket.number)
        repair.save()

        if repair.end_date and not self.old_end_date:
            techstate_status = get_object_or_404(TechStateOption, name='Ремонта не требует')
            BucketTechState.objects.create(
                bucket=bucket,
                date=repair.end_date,
                techstate=techstate_status,
                is_operable=True,
                author=self.request.user,
            )
            messages.success(self.request, 'Ремонт успешно завершен! Техсостояние обновлено!')
        else:
            messages.success(self.request, 'Ремонт успешно обновлен!')

        return redirect('bucket_repairs_tab', bucket_number=bucket.number)
