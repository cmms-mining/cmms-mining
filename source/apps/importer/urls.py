from django.urls import path

from apps.importer import views


urlpatterns = [
    path('', views.ExcelImportView.as_view(), name='importer'),
]
