from django.urls import path

from apps.importer import views


urlpatterns = [
    path('', views.ExcelUploadView.as_view(), name='importer'),
]
