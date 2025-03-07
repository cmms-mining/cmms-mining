from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView

from apps.contractors.models import Appendix, Contract

from ..forms import AppendixCreateForm


class AppendixCreateView(CreateView):
    model = Appendix
    form_class = AppendixCreateForm
    template_name = 'contracts/appendix_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contract = get_object_or_404(Contract, pk=self.kwargs.get('contract_pk'))
        context['contract'] = contract
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'contract': self.kwargs.get('contract_pk')}
        return kwargs

    def form_valid(self, form):
        appendix: Appendix = form.save()
        contractor_pk = appendix.contract.contractor.pk
        return redirect('contractor', contractor_pk=contractor_pk)
