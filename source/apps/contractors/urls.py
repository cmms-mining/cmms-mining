from django.urls import path

from .views import contractors


urlpatterns = [
    path('', contractors.ContractorsListView.as_view(), name='contractors'),
]
