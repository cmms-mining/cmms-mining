from apps.equipments.models import Equipment


def get_equip_without_document(document_type: str):
    """Получает из базы список оборудования, для которого не прикреплен документ"""
    equipments = Equipment.objects.exclude(equipment_documents__document_type__slug=document_type).distinct()
    return equipments
