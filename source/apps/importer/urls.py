from django.urls import path

from apps.importer import views


urlpatterns = [
    path('', views.ImporterView.as_view(), name='importer'),
    path('excel-upload', views.ExcelUploadView.as_view(), name='excel_upload'),
    path('google-connect', views.GoogleConnectView.as_view(), name='google_connect'),
]
