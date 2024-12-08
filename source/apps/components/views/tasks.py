from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.common.bot import notify_telegram
from apps.components.forms import ComponentTaskCommentForm, ComponentTaskCreateForm, ComponentTaskUpdateForm
from apps.components.models import Component, ComponentTask


class ComponentTasksListView(TemplateView):
    template_name = 'components/tasks/component_tasks_tab.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['tasks_tab'] = True
        return context


class ComponentTaskCreateView(CreateView):
    model = ComponentTask
    form_class = ComponentTaskCreateForm
    template_name = 'components/tasks/component_task_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        context['component'] = component
        context['tasks_tab'] = True
        return context

    def form_valid(self, form):
        task: ComponentTask = form.save(commit=False)
        component = get_object_or_404(Component, number=self.kwargs.get('component_number'))
        task.component = component
        task.task_type = 'component'
        task.save()
        messages.success(self.request, 'Задача успешно создана!')
        return redirect('component_tasks_tab', component_number=task.component.number)


class ComponentTaskUpdateView(UpdateView):
    model = ComponentTask
    form_class = ComponentTaskUpdateForm
    template_name = 'components/tasks/component_task_update.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """ Если задачу открыл исполнитель, ставим статус - задача прочитана """
        task = self.get_object()
        if request.user == task.executor:
            task.has_been_read = True
            task.save()
        return super().get(request, *args, **kwargs)

    def get_object(self) -> ComponentTask:
        if not hasattr(self, '_object'):
            self._object = get_object_or_404(ComponentTask, pk=self.kwargs.get('task_pk'))
        return self._object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['task'] = task
        context['component'] = task.component
        context['comment_form'] = ComponentTaskCommentForm()
        context['tasks_tab'] = True
        return context

    def form_valid(self, form):
        task: ComponentTask = form.save(commit=False)

        if task.completed and not task.completed_at:
            task.completed_at = timezone.localtime().date()
            messages.success(self.request, 'Задача успешно закрыта!')
        else:
            messages.warning(self.request, 'Задача успешно отредактирована!')

        if not task.completed:
            task.completed_at = None

        task.save()

        bot_message = f'{self.request.user.get_full_name()} отредактировал задачу {task.name}'
        relative_url = reverse('component_task_update', args=[task.pk])
        full_url = self.request.build_absolute_uri(relative_url)
        bot_message += '\n' + full_url
        notify_telegram(message=bot_message)

        return redirect('component_tasks_tab', component_number=task.component.number)
