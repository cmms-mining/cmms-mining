from apps.equipments.models import Equipment
from apps.maintenance.models import (MaintenanceCardItem, MaintenanceCategory,
                                     ScheduledMaintenanceWork,
                                     ScheduledMaintenanceWorkSystem)


def get_systems_by_equipment_and_maintenance_category(equipment: Equipment, maintenance_category: MaintenanceCategory):
    maintenance_card_items = MaintenanceCardItem.objects.filter(
                            equipment_maintenance_group=equipment.equipment_maintenance_group,
                            maintenance_category=maintenance_category,
                        )
    scheduled_maintenance_works = ScheduledMaintenanceWork.objects.filter(
                            maintenance_card_items__in=maintenance_card_items,
                        )

    systems = ScheduledMaintenanceWorkSystem.objects.filter(
                            maintenance_works__in=scheduled_maintenance_works,
                        ).distinct()
    return systems


def get_maintenance_categories_by_equipment(equipment: Equipment):
    maintenance_card_items = equipment.equipment_maintenance_group.maintenance_card_items.all()
    maintenance_categories = MaintenanceCategory.objects.filter(
                            maintenance_card_items__in=maintenance_card_items,
                        ).distinct()
    return maintenance_categories
