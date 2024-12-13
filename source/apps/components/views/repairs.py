from django.views.generic import ListView

from ..models import ComponentRepair


class ComponentsRepairsListView(ListView):
    model = ComponentRepair
    template_name = 'components/repairs/repairs_list.html'
    context_object_name = 'repairs'
