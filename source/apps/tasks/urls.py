from django.urls import path

from . import views


urlpatterns = [
    path('', views.TasksListView.as_view(), name='tasks'),

    path(
        '<int:task_pk>/update',
        views.TaskUpdateView.as_view(),
        name='task_update',
        ),
    path(
        '<int:task_pk>/comment/create',
        views.TaskCommentCreate.as_view(),
        name='task_comment_create',
        ),
]
