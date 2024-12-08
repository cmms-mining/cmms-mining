from django.urls import path

from apps.equip_documents import views


urlpatterns = [
    path('no-catalogs/', views.EquipNoCatalogsView.as_view(), name='no_catalogs'),
]
