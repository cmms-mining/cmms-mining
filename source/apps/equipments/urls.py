from django.urls import path

from .views import equipments, orders, relocations


urlpatterns = [
    path('', equipments.EquipmentsListView.as_view(), name='equipments'),
    path(
        route='<slug:equipment_number>/all-events',
        view=equipments.EquipmentAllEventsView.as_view(),
        name='equipment_all_events_tab',
        ),

    # Перемещения оборудования
    path(
        'relocations',
        relocations.EquipmentsRelocationsListView.as_view(),
        name='equipments_relocations',
        ),

    path(
        '<slug:equipment_number>/relocations',
        relocations.EquipmentRelocationsTabView.as_view(),
        name='equipment_relocations_tab',
        ),
    path(
        '<slug:equipment_number>/relocation/create',
        relocations.EquipmentRelocationCreateView.as_view(),
        name='equipment_relocation_create',
        ),
    path(
        'relocation/<int:equipment_relocation_pk>/update',
        relocations.EquipmentRelocationUpdateView.as_view(),
        name='equipment_relocation_update',
        ),
    path(
        'relocation/<int:equipment_relocation_pk>/add-attachment',
        relocations.EquipmentRelocationAddAttachmentView.as_view(),
        name='equipment_relocation_attachment_add',
        ),
    path(
        'relocation/<int:equipment_relocation_pk>/add-date',
        relocations.EquipmentRelocationDateAddView.as_view(),
        name='equipment_relocation_date_add',
        ),

    path(
        'relocations-orders',
        orders.RelocationsOrdersListView.as_view(),
        name='equipments_relocations_orders',
        ),
    path(
        'relocation-order-create',
        orders.RelocationOrderCreateView.as_view(),
        name='equipment_relocation_order_create',
        ),
    path(
        'relocation-order/<int:order_pk>/update',
        orders.RelocationOrderUpdateView.as_view(),
        name='equipment_relocation_order_update',
        ),
    path(
        'relocation-order/<int:order_pk>/add-equipment',
        orders.RelocationOrderAddEquipmentView.as_view(),
        name='relocation_order_add_equipment',
        ),
    path(
        'relocation-order/<int:order_pk>/add-equipment-relocations',
        orders.EquipmentRelocationCreateByOrderView.as_view(),
        name='equipment_relocation_create_by_order',
        ),
    path(
        'relocation-order/<int:order_pk>/update-status',
        orders.RelocationOrderUpdateStatusView.as_view(),
        name='equipment_relocation_update_status',
        ),
]
