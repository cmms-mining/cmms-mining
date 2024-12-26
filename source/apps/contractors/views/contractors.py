from django.views.generic import ListView

from apps.contractors.models import Contractor


class ContractorsListView(ListView):
    model = Contractor
    context_object_name = 'contractors'
    template_name = 'contractors/contractors_list.html'
