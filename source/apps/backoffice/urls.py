from django.urls import path

from apps.backoffice.views import useraction


urlpatterns = [
    path('', useraction.UsersActionsView.as_view(), name='users_actions'),
    path(
        'set-buckets-requires-reconciliation',
        useraction.set_buckets_requires_reconciliation,
        name='set_buckets_requires_reconciliation',
        ),
    path(
        'refresh-component-current-data',
        useraction.refresh_component_current_data,
        name='refresh_component_current_data',
        ),
]
