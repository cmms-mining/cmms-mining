from django.views.generic import TemplateView

from apps.equip_documents.services import get_equip_without_document


class EquipNoCatalogsView(TemplateView):
    """Список оборудования без каталогов"""
    template_name = 'no_catalogs.html'

    def get_context_data(self, **kwargs) -> dict:
        context: dict = super().get_context_data(**kwargs)
        context['equip_without_commissioning_sheet'] = get_equip_without_document('commissioning_sheet')
        context['equip_without_acceptance_act'] = get_equip_without_document('acceptance_act')
        context['equip_without_nameplate'] = get_equip_without_document('nameplate')
        context['equip_without_pneumatic'] = get_equip_without_document('pneumatic')
        context['equip_without_hydraulic'] = get_equip_without_document('hydraulic')
        context['equip_without_electric'] = get_equip_without_document('electric')
        context['equip_without_manual'] = get_equip_without_document('manual')
        context['equip_without_catalog'] = get_equip_without_document('catalog')
        return context
