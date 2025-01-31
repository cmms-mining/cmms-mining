from django.urls import path

from . import views


urlpatterns = [
    path('', views.DocumentsListView.as_view(), name='documents'),
]
