from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView

from apps.contractors.models import Contractor


class ContractorsListView(ListView):
    model = Contractor
    context_object_name = 'contractors'
    template_name = 'contractors/contractors_list.html'


class ContractorDetailView(DetailView):
    context_object_name = 'contractor'
    template_name = 'contractors/contractor_detail.html'

    def get_object(self):
        return get_object_or_404(Contractor, pk=self.kwargs.get('contractor_pk'))
