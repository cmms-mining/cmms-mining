from itertools import chain
from typing import Any

from django.db.models import CharField, Q, QuerySet, Value
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

import pandas as pd

from apps.buckets.models import (
    Bucket, BucketDeinstallation, BucketInstallation, BucketReconciliation, BucketRelocation, BucketRepair,
    BucketTechState,
)
from apps.buckets.services import (add_decommission_to_buckets_qs, add_equipment_to_buckets_qs,
                                   add_location_to_buckets_qs, add_repair_to_buckets_qs, add_techstate_to_buckets_qs,
                                   filter_buckets_by_decommissioned)


class BucketsListView(ListView):
    model = Bucket
    context_object_name = 'buckets'
    template_name = 'buckets/buckets_list.html'

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Bucket.objects.select_related(
            'current_data',
            'current_data__location',
            'current_data__equipment',
            'current_data__techstate',
        ).all().filter(Q(decommission__decommissioned=False) | Q(decommission__isnull=True))
        return queryset


class BucketAllEventsView(DetailView):
    context_object_name = 'bucket'
    template_name = 'buckets/bucket_all_events_tab.html'

    def get_object(self):
        return get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['all_events_tab'] = True
        bucket_id = self.get_object().pk

        # Получаем перемещения для конкретного Bucket
        relocations = BucketRelocation.objects.filter(
            bucket_id=bucket_id).values('date').annotate(
                event_type=Value('Перемещение', output_field=CharField()))

        # Получаем тех. состояния для конкретного Bucket
        tech_states = BucketTechState.objects.filter(
            bucket_id=bucket_id).values('date').annotate(
                event_type=Value('Техсостояние', output_field=CharField()))

        # Получаем сверки для конкретного Bucket
        reconciliations = BucketReconciliation.objects.filter(
            bucket_id=bucket_id).values('date').annotate(
                event_type=Value('Сверка', output_field=CharField()))

        # Получаем установки для конкретного Bucket
        installations = BucketInstallation.objects.filter(
            bucket_id=bucket_id).values('date').annotate(
                event_type=Value('Установка', output_field=CharField()))

        # Получаем демонтажи для конкретного Bucket
        deinstallations = BucketDeinstallation.objects.filter(
            bucket_id=bucket_id).values('date').annotate(
                event_type=Value('Демонтаж', output_field=CharField()))

        # Получаем ремонты для конкретного Bucket
        repairs = BucketRepair.objects.filter(
            bucket_id=bucket_id).values('date').annotate(
                event_type=Value('Ремонт', output_field=CharField()))

        # Объединяем все QuerySet и сортируем по дате
        events = sorted(
            chain(relocations, tech_states, reconciliations, installations, deinstallations, repairs),
            key=lambda event: event['date'],
            reverse=True,
        )
        context['events'] = events

        return context


def export_bukets_to_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="buckets.xlsx"'

    buckets_qs = Bucket.objects.all().values('number', 'capacity__capacity', 'tooth_adapter__name',
                                             'manufacturer__name', 'production_year', 'nomencl_code',
                                             'equipment_model__name')
    buckets_qs = filter_buckets_by_decommissioned(buckets_qs=buckets_qs)
    buckets_qs = add_location_to_buckets_qs(buckets_qs=buckets_qs)
    buckets_qs = add_techstate_to_buckets_qs(buckets_qs=buckets_qs)
    buckets_qs = add_equipment_to_buckets_qs(buckets_qs=buckets_qs)
    buckets_qs = add_repair_to_buckets_qs(buckets_qs=buckets_qs)
    buckets_qs = add_decommission_to_buckets_qs(buckets_qs=buckets_qs)

    df = pd.DataFrame(list(buckets_qs))
    df = df.rename(columns={
        'number': 'Номер',
        'capacity__capacity': 'Объем',
        'tooth_adapter__name': 'Адаптер',
        'manufacturer__name': 'Производитель',
        'production_year': 'Год производства',
        'nomencl_code': 'Код номенклатуры',
        'equipment_model__name': 'Модель оборудования',
        'latest_site': 'Местоположение',
        'techstate_name': 'Техсостояние',
        'is_operable': 'Подлежит эксплуатации',
        'techstate_description': 'Описание техсостояния',
        'current_equipment': 'Установлен на',
        'start_date': 'Дата начала ремонта',
        'end_date': 'Дата окончания ремонта',
        'plan_start_date': 'Плановая дата начала ремонта',
        'plan_end_date': 'Плановая дата окончания ремонта',
        'worklist': 'Требуемые работы по ремонту',
        'obsoleted': 'Выведен из эксплуатации',
        })
    df['Подлежит эксплуатации'] = df['Подлежит эксплуатации'].replace(False, 'НЕТ')
    df['Подлежит эксплуатации'] = df['Подлежит эксплуатации'].replace(True, '')
    df['Выведен из эксплуатации'] = df['Выведен из эксплуатации'].replace(True, 'ДА')
    df['Выведен из эксплуатации'] = df['Выведен из эксплуатации'].replace(False, '')

    df.to_excel(response, index=False)  # index=False, чтобы не сохранять индексы DataFrame в файл
    return response
