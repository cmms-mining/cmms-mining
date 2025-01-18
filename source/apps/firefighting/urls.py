from django.urls import path

from . import views


urlpatterns = [
    path('', views.FirefightingsListView.as_view(), name='firefightings'),
    path(
        '<int:equipment_number>/create-check',
        views.FirefightingCheckCreateView.as_view(),
        name='firefighting_check_create',
        ),
]
