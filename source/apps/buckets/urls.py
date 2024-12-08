from django.urls import path

from apps.buckets.views import buckets, installations, reconciliations, relocations, repairs, techstates


urlpatterns = [
    path('', buckets.BucketsListView.as_view(), name='buckets'),
    path('<slug:bucket_number>/all-events', buckets.BucketAllEventsView.as_view(), name='bucket_all_events_tab'),

    # Перемещения ковшей
    path(
        '<slug:bucket_number>/relocations',
        relocations.BucketRelocationsTabView.as_view(),
        name='bucket_relocations_tab',
        ),
    path(
        '<slug:bucket_number>/relocation/create',
        relocations.BucketRelocationCreateView.as_view(),
        name='bucket_relocation_create',
        ),
    path(
        '<slug:bucket_number>/relocation/<int:relocation_pk>/attachment_create',
        relocations.BucketRelocationAttachmentCreateView.as_view(),
        name='bucket_relocation_attachment_create',
        ),

    # Техсостояния ковшей
    path(
        '<slug:bucket_number>/techstates',
        techstates.BucketTechStatesListView.as_view(),
        name='bucket_techstates_tab',
        ),
    path(
        '<slug:bucket_number>/techstate/create',
        techstates.BucketTechStatesCreateView.as_view(),
        name='bucket_techstate_create',
        ),
    path(
        '<slug:bucket_number>/techstate/<int:techstate_pk>/update',
        techstates.BucketTechStatesUpdateView.as_view(),
        name='bucket_techstate_update',
        ),

    # Ремонты ковшей
    path(
        '<slug:bucket_number>/repairs',
        repairs.BucketRepairsListView.as_view(),
        name='bucket_repairs_tab',
        ),
    path(
        '<slug:bucket_number>/repairs/create',
        repairs.BucketRepairCreateView.as_view(),
        name='bucket_repair_create',
        ),
    path(
        '<slug:bucket_number>/repairs/<int:repair_pk>/update',
        repairs.BucketRepairUpdateView.as_view(),
        name='bucket_repair_update',
        ),

    # Сверки ковшей
    path(
        '<slug:bucket_number>/reconciliations',
        reconciliations.BucketReconciliationsTabView.as_view(),
        name='bucket_reconciliations_tab',
        ),
    path(
        '<slug:bucket_number>/reconciliations/create',
        reconciliations.BucketReconciliationCreateView.as_view(),
        name='bucket_reconciliation_create',
        ),
    path(
        '<slug:bucket_number>/reconciliations/invalid',
        reconciliations.BucketReconciliationInvalidView.as_view(),
        name='bucket_reconciliation_invalid',
        ),

    # Установки ковшей
    path(
        '<slug:bucket_number>/installations',
        installations.BucketInstallationsTabView.as_view(),
        name='bucket_installations_tab',
        ),
    path(
        '<slug:bucket_number>/deinstallation/create',
        installations.BucketDeinstallationCreateView.as_view(),
        name='bucket_deinstallation_create',
        ),
    path(
        '<slug:bucket_number>/installation/create',
        installations.BucketInstallationCreateView.as_view(),
        name='bucket_installation_create',
        ),
    path(
        'deinstallation/<int:pk>/delete',
        installations.BucketDeinstallationDeleteView.as_view(),
        name='bucket_deinstallation_delete',
        ),
    path(
        'installation/<int:pk>/delete',
        installations.BucketInstallationDeleteView.as_view(),
        name='bucket_installation_delete',
        ),

    # Выгрузка в эксель
    path('export', buckets.export_bukets_to_excel, name='buckets_export'),

]
