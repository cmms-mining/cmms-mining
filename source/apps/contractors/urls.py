from django.urls import path

from .views import contractors


urlpatterns = [
    path('', contractors.ContractorsListView.as_view(), name='contractors'),
    path('<int:contractor_pk>', contractors.ContractorDetailView.as_view(), name='contractor'),
]
