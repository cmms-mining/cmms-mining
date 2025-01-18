from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.accounts.urls')),
    path('', lambda request: redirect('tasks', permanent=False)),
    path('backoffice/', include('apps.backoffice.urls')),
    path('buckets/', include('apps.buckets.urls')),
    path('catalogs/', include('apps.equip_documents.urls')),
    path('components/', include('apps.components.urls')),
    path('contractors/', include('apps.contractors.urls')),
    path('equipments/', include('apps.equipments.urls')),
    path('firefighting/', include('apps.firefighting.urls')),
    path('importer/', include('apps.importer.urls')),
    path('tasks/', include('apps.tasks.urls')),

    path('__debug__/', include('debug_toolbar.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
