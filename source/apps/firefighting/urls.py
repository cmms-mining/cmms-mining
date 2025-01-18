from django.urls import path

from . import views


urlpatterns = [
    path('', views.FirefightingsListView.as_view(), name='firefightings'),
]
