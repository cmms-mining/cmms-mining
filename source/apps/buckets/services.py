from django.contrib.auth.models import User
from django.db.models import CharField, Count, Exists, F, OuterRef, Q, Subquery, Value
from django.db.models.functions import Coalesce
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils import timezone

from apps.buckets.models import (Bucket, BucketDeinstallation, BucketInstallation, BucketRelocation,
                                 BucketRepair, BucketTechState)
from apps.common.models import DeinstallationReason, TechStateOption
from apps.equipments.models import Equipment
from apps.sites.models import WorkCenter


def get_buckets_to_reconciliation(workcenter: str | None, site: str | None) -> QuerySet:
    buckets_with_location = get_buckets_with_location(workcenter, site)
    buckets_to_reconciliation = buckets_with_location.filter(
        requires_reconciliation=True,
    ).distinct()
    result_queryset = filter_buckets_by_decommissioned(buckets_qs=buckets_to_reconciliation)
    return result_queryset.distinct()


def get_buckets_with_location(workcenter: str | None, site: str | None) -> QuerySet:
    """Возвращает все ковши с полем последнего местоположения (str) с фильтром по участку или проекту"""
    buckets = Bucket.objects.all()
    buckets_with_latest_location = add_location_to_buckets_qs(buckets_qs=buckets)
    filtered_buckets_with_latest_location = filter_buckets_by_workcenter_or_site(
        buckets_qs=buckets_with_latest_location,
        workcenter=workcenter,
        site=site,
        )
    return filtered_buckets_with_latest_location


def add_location_to_buckets_qs(buckets_qs: QuerySet) -> QuerySet:
    latest_relocations = BucketRelocation.objects.filter(bucket=OuterRef('pk'))
    latest_locations = latest_relocations.values('to_site_id__name')[:1]
    buckets_qs_with_location = buckets_qs.annotate(
        latest_site=Subquery(latest_locations),
    )
    return buckets_qs_with_location


def add_techstate_to_buckets_qs(buckets_qs: QuerySet) -> QuerySet:
    latest_techstates = BucketTechState.objects.filter(bucket=OuterRef('pk'))
    techstate_name = latest_techstates.values('techstate__name')[:1]
    is_operable = latest_techstates.values('is_operable')[:1]
    techstate_description = latest_techstates.values('description')[:1]
    result = buckets_qs.annotate(
        techstate_name=Subquery(techstate_name),
        is_operable=Subquery(is_operable),
        techstate_description=Subquery(techstate_description),
    )
    return result


def add_decommission_to_buckets_qs(buckets_qs: QuerySet) -> QuerySet:
    buckets_qs = buckets_qs.annotate(
        obsoleted=Coalesce(F('decommission__obsoleted'), Value(False)),
    )
    return buckets_qs


def add_repair_to_buckets_qs(buckets_qs: QuerySet) -> QuerySet:
    repairs = BucketRepair.objects.filter(bucket=OuterRef('pk'))
    start_date = repairs.values('start_date')[:1]
    end_date = repairs.values('end_date')[:1]
    plan_start_date = repairs.values('plan_start_date')[:1]
    plan_end_date = repairs.values('plan_end_date')[:1]
    worklist = repairs.values('worklist')[:1]
    result = buckets_qs.annotate(
        start_date=Subquery(start_date),
        end_date=Subquery(end_date),
        plan_start_date=Subquery(plan_start_date),
        plan_end_date=Subquery(plan_end_date),
        worklist=Subquery(worklist),
    )
    return result


def add_equipment_to_buckets_qs(buckets_qs: QuerySet) -> QuerySet:
    # Подзапрос на последнее установленное оборудование
    last_installation_subquery = BucketInstallation.objects.filter(
        bucket=OuterRef('pk'),
    ).order_by('-date').values('to_equipment__number')[:1]

    # Подзапрос на проверку, есть ли демонтаж для ковша
    deinstallation_exists_subquery = BucketDeinstallation.objects.filter(
        bucket=OuterRef('pk'),
    )
    # Аннотация текущим оборудованием
    result = buckets_qs.annotate(
        current_equipment=Subquery(last_installation_subquery),
        ).filter(
            ~Exists(deinstallation_exists_subquery),  # Используем отрицание Exists
        )

    return result


def get_combined_installs_and_deinstalls(bucket: Bucket) -> list[dict[str, str]]:
    """Получаем все установки и демонтажи ковша"""

    installations = BucketInstallation.objects.filter(bucket=bucket).values(
        'pk',
        'to_equipment',
        'date',
        'author',
    ).annotate(
            from_equipment=Value(None, output_field=CharField()),
        )

    deinstallations = BucketDeinstallation.objects.filter(bucket=bucket).values(
        'pk',
        'from_equipment',
        'date',
        'reason',
        'author',
    ).annotate(
            to_equipment=Value(None, output_field=CharField()),
        )

    combined_queryset = list(installations) + list(deinstallations)

    combined_queryset = sorted(combined_queryset, key=lambda x: x['date'], reverse=True)

    for item in combined_queryset:
        item['author'] = get_object_or_404(User, pk=item['author'])
        if item.get('reason'):
            item['reason'] = get_object_or_404(DeinstallationReason, pk=item['reason'])
        if item.get('to_equipment'):
            item['to_equipment'] = Equipment.objects.get(pk=item['to_equipment']).number
        if item.get('from_equipment'):
            item['from_equipment'] = Equipment.objects.get(pk=item['from_equipment']).number

    if combined_queryset:
        if combined_queryset[0].get('from_equipment'):
            combined_queryset[0]['is_edit_allowed'] = get_object_or_404(
                BucketDeinstallation,
                pk=combined_queryset[0].get('pk'),
                ).is_edit_allowed()
        if combined_queryset[0].get('to_equipment'):
            combined_queryset[0]['is_edit_allowed'] = get_object_or_404(
                BucketInstallation,
                pk=combined_queryset[0].get('pk'),
                ).is_edit_allowed()

    return combined_queryset


def get_defect_buckets_without_repair(workcenter: str | None, site: str | None) -> QuerySet:
    buckets_with_location = get_buckets_with_location(workcenter=workcenter, site=site)

    # Получаем подзапрос для последнего техсостояния ковша
    last_tech_state_subquery = BucketTechState.objects.filter(
        bucket=OuterRef('pk'),
    ).values('techstate')[:1]

    repair_required_state_current = TechStateOption.objects.get(name="Требует текущего ремонта")
    repair_required_state_capital = TechStateOption.objects.get(name="Требует капитального ремонта")
    # Выбираем ковши, у которых последнее состояние "Требует текущего ремонта" или "Требует капитального ремонта"
    buckets_requiring_repair = buckets_with_location.annotate(
        last_techstate=Subquery(last_tech_state_subquery),
    ).filter(
        Q(last_techstate=repair_required_state_current) | Q(last_techstate=repair_required_state_capital),
    )

    # Аннотируем к ковшам, требующим ремонта количество созданных ремонтов
    buckets_with_repair_count = buckets_requiring_repair.annotate(
        repair_count=Count('repairs'),
    )
    defect_buckets_without_repair = buckets_with_repair_count.filter(
        repair_count=0,
    ) | buckets_with_repair_count.exclude(repairs__end_date__isnull=True)

    return defect_buckets_without_repair


def get_buckets_without_repair_start_date(workcenter: str | None, site: str | None) -> QuerySet:
    buckets_with_location = get_buckets_with_location(workcenter=workcenter, site=site)

    buckets_without_repair_start_date = buckets_with_location.filter(
        repairs__start_date__isnull=True,      # Нет фактической даты начала ремонта
        repairs__plan_start_date__isnull=True,  # Нет плановой даты начала ремонта
        repairs__isnull=False,  # У ковша должна быть хотя бы одна запись о ремонте
        repairs__end_date__isnull=True,  # Запись ремонта активна (нет даты окончания)
        )

    return buckets_without_repair_start_date


def get_buckets_with_expired_repair_start_date(workcenter: str | None, site: str | None) -> QuerySet:
    """Ковши, по которым прошла плановая дата начала ремонта, но ремонт не начался"""
    buckets_with_location = get_buckets_with_location(workcenter=workcenter, site=site)

    buckets_with_expired_repair_start_date = buckets_with_location.filter(
        repairs__start_date__isnull=True,      # Нет фактической даты начала ремонта
        repairs__plan_start_date__lt=timezone.localtime().date(),  # Плановая дата начала уже прошла
        )
    return buckets_with_expired_repair_start_date


def get_buckets_with_expired_repair_plan_end_date(workcenter: str | None, site: str | None) -> QuerySet:
    """Ковши, по которым прошла плановая дата окончания ремонта, но ремонт не окончен"""
    buckets_with_location = get_buckets_with_location(workcenter=workcenter, site=site)
    buckets_with_expired_repair_end_date = buckets_with_location.filter(
        repairs__end_date__isnull=True,      # Нет фактической даты окончания ремонта
        repairs__plan_end_date__lt=timezone.localtime().date(),  # Плановая дата окончания уже прошла
        )
    return buckets_with_expired_repair_end_date


def filter_buckets_by_workcenter_or_site(
        buckets_qs: QuerySet,
        workcenter: str | None,
        site: str | None) -> QuerySet:

    if workcenter:
        workcenter_instance = get_object_or_404(WorkCenter, name=workcenter)
        site_names = workcenter_instance.sites.values_list('name', flat=True)
        filtered_buckets = buckets_qs.filter(latest_site__in=site_names)
    elif site:
        filtered_buckets = buckets_qs.filter(latest_site=site)
    else:
        return buckets_qs

    return filtered_buckets


def filter_buckets_by_decommissioned(buckets_qs: QuerySet) -> QuerySet:
    result = buckets_qs.exclude(decommission__decommissioned=True)
    return result
