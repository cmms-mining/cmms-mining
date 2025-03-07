from django.urls import path

from .views import contractors, contracts


urlpatterns = [
    path('', contractors.ContractorsListView.as_view(), name='contractors'),
    path('<int:contractor_pk>', contractors.ContractorDetailView.as_view(), name='contractor'),

    path('contract/<int:contract_pk>/appendix-create', contracts.AppendixCreateView.as_view(), name='appendix_create'),
]
