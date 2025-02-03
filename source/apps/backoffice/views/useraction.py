from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.backoffice.mixins import SuperuserRequiredMixin
from apps.backoffice.services import get_db_size, get_disk_space, get_memory_info
from apps.buckets.models import (
    Bucket, BucketDeinstallation, BucketInstallation, BucketReconciliation, BucketRelocation, BucketRepair,
    BucketTechState,
)


class UsersActionsView(SuperuserRequiredMixin, TemplateView):
    """Список действий пользователей"""
    template_name = 'backoffice/users_actions.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        buckets_relocations = BucketRelocation.objects.all()
        context['buckets_relocations'] = buckets_relocations

        buckets_reconciliations = BucketReconciliation.objects.all()
        context['buckets_reconciliations'] = buckets_reconciliations

        buckets_techstates = BucketTechState.objects.all()
        context['buckets_techstates'] = buckets_techstates

        buckets_deinstallations = BucketDeinstallation.objects.all()
        context['buckets_deinstallations'] = buckets_deinstallations

        buckets_installations = BucketInstallation.objects.all()
        context['buckets_installations'] = buckets_installations

        buckets_repairs = BucketRepair.objects.all()
        context['buckets_repairs'] = buckets_repairs

        context['db_size'] = get_db_size()
        context['disk_space'] = get_disk_space()
        context['memory_info'] = get_memory_info()

        return context


def set_buckets_requires_reconciliation(request):
    buckets = Bucket.objects.all()
    for bucket in buckets:
        #  Можно устанавливать статус "требуется сверка" и без проверки текущего состояния,
        #  но тогда будут перезаписываться все записи, в том числе и выставленные вручную для принудительной сверки
        if bucket.requires_reconciliation is not True:
            bucket.requires_reconciliation = True if bucket.is_to_reconciliate() else False
            bucket.save()
    return redirect('users_actions')
