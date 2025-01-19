from django.urls import path

from . import views


urlpatterns = [
    path('', views.FirefightingsListView.as_view(), name='firefightings'),
    path(
        '<str:equipment_number>/create-check',
        views.FirefightingCheckCreateView.as_view(),
        name='firefighting_check_create',
        ),
    path(
        '<str:firefighting_check_pk>/update-check',
        views.FirefightingCheckUpdateView.as_view(),
        name='firefighting_check_update',
        ),
]
