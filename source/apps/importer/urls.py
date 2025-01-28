from django.urls import path

from apps.importer import views


urlpatterns = [
    path('', views.ImporterView.as_view(), name='importer'),
    path('excel-upload', views.ExcelNomenclatureLoadView.as_view(), name='excel_upload'),
    path('google-connect', views.ImportRunningTimeGoogleView.as_view(), name='google_connect'),
]
