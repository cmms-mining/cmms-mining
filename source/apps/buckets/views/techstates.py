from typing import Any

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.buckets.forms import BucketTechStateForm
from apps.buckets.models import Bucket, BucketTechState


class FormValidationMixin:
    def validate_form(self, form):
        new_techstate_date = self.techstate.date
        bucket: Bucket = self.techstate.bucket

        if isinstance(self, BucketTechStatesCreateView) and bucket.get_techstate():
            # проверка даты, должна быть не меньше и не равна дате предыдущего техсостояния
            last_techstate_date = bucket.get_techstate().date
            if new_techstate_date <= last_techstate_date:
                messages.warning(
                    self.request,
                    'Дата техсостояния не может быть меньше или равна дате предыдущего техсостояния!',
                    )
                return False

        if isinstance(self, BucketTechStatesUpdateView):
            if not self.techstate.is_edit_allowed():
                messages.warning(self.request, 'Ошибка - редактирование разрешено только для последнего техсостояния!')
                return False
            if len(BucketTechState.objects.filter(bucket=bucket)) > 1:
                second_techstate = BucketTechState.objects.filter(bucket=bucket)[1]
                if new_techstate_date <= second_techstate.date:
                    messages.warning(
                        self.request,
                        'Ошибка - дата техсостояния не может быть меньше или равна дате предыдущего техсостояния!',
                        )
                    return False
        # TODO добавить возможность редактирования только автору техсостояния и в день создания
        # (проверяется на уровне ссылки на редактирование)

        if new_techstate_date > timezone.localtime().date():
            messages.warning(self.request, 'Ошибка - дата техсостояния не может быть больше текущей даты!')
            return False

        if bucket.get_is_being_repaired() and self.techstate.techstate.name == 'Ремонта не требует':
            messages.warning(
                self.request,
                'Ошибка - статус "Ремонта не требует" нельзя установить находящемуся в ремонте ковшу!',
                )
            return False

        if not self.techstate.is_operable and self.techstate.techstate.name == 'Ремонта не требует':
            messages.warning(
                self.request,
                'Ошибка - ковш, не требующий ремонта должен подлежать эксплуатации!',
                )
            return False

        return True


class BucketTechStatesListView(TemplateView):
    """Список техсостояний"""
    template_name = 'buckets/techstates/bucket_techstates_tab.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['bucket'] = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['techstates_tab'] = True
        return context


class BucketTechStatesCreateView(FormValidationMixin, CreateView):
    model = BucketTechState
    form_class = BucketTechStateForm
    template_name = 'buckets/techstates/bucket_techstate_create.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        context['techstates_tab'] = True
        return context

    def form_valid(self, form):
        techstate: BucketTechState = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        techstate.bucket = bucket
        self.techstate = techstate

        if not self.validate_form(form):
            return redirect('bucket_techstates_tab', bucket_number=bucket.number)

        techstate.author = self.request.user

        techstate.save()
        messages.success(self.request, 'Техсостояние успешно изменено!')
        return redirect('bucket_techstates_tab', bucket_number=techstate.bucket.number)


class BucketTechStatesUpdateView(FormValidationMixin, UpdateView):
    form_class = BucketTechStateForm
    context_object_name = 'techstate'
    template_name = 'buckets/techstates/bucket_techstate_update.html'

    def get_object(self):
        return get_object_or_404(BucketTechState, pk=self.kwargs.get('techstate_pk'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['bucket'] = self.object.bucket
        context['techstates_tab'] = True
        return context

    def form_valid(self, form):
        techstate: BucketTechState = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        techstate.bucket = bucket
        self.techstate = techstate

        if not self.validate_form(form):
            return redirect('bucket_techstates_tab', bucket_number=bucket.number)

        techstate.save()
        messages.success(self.request, 'Техсостояние успешно обновлено!')
        return redirect('bucket_techstates_tab', bucket_number=techstate.bucket.number)
