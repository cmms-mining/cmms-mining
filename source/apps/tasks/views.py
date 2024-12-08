from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView, TemplateView, UpdateView

from apps.buckets.services import (
    get_buckets_to_reconciliation, get_buckets_with_expired_repair_plan_end_date,
    get_buckets_with_expired_repair_start_date, get_buckets_without_repair_start_date,
    get_defect_buckets_without_repair,
    )
from apps.common.bot import notify_telegram
from apps.components.models import ComponentTask
from apps.tasks.forms import TaskCommentForm, TaskUpdateForm
from apps.tasks.models import Task, TaskComment


class TasksListView(TemplateView):
    template_name = 'tasks/tasks_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        workcenter = None
        site = None

        if self.request.user.groups.all():
            if self.request.user.groups.first().customgroup.workcenter:
                workcenter = self.request.user.groups.first().customgroup.workcenter.name
            if self.request.user.groups.first().customgroup.site:
                site = self.request.user.groups.first().customgroup.site.name

        context['buckets_to_reconciliation'] = get_buckets_to_reconciliation(workcenter=workcenter, site=site)

        # ковши, которые требуют ремонта, но ремонт не оформлен
        context['defect_buckets_without_repair'] = get_defect_buckets_without_repair(workcenter=workcenter, site=site)

        context['buckets_without_repair_start_date'] = get_buckets_without_repair_start_date(
                                                                                        workcenter=workcenter,
                                                                                        site=site,
                                                                                        )

        context['buckets_with_expired_repair_start_date'] = get_buckets_with_expired_repair_start_date(
                                                                                        workcenter=workcenter,
                                                                                        site=site,
                                                                                        )
        # ковши, по которым прошла плановая дата окончания ремонта
        context['buckets_with_expired_repair_plan_end_date'] = get_buckets_with_expired_repair_plan_end_date(
                                                                                        workcenter=workcenter,
                                                                                        site=site,
                                                                                        )
        components_tasks = ComponentTask.objects.filter(verified=False)
        if self.request.user.is_superuser:
            pass
        elif self.request.user.groups.filter(name='Головной офис').exists():
            components_tasks = components_tasks.exclude(executor__is_superuser=True)
        else:
            components_tasks = components_tasks.exclude(executor__is_superuser=True).filter(executor=self.request.user)

        components_tasks = components_tasks.values(
            'pk',
            'name',
            'executor__first_name',
            'executor__last_name',
            'component__number',
            'component__nomenclature_code',
            'component__component_type__name',
            'component__current_data__location__name',
            'created_at',
            'planned_completion_date',
            'completed',
            'needs_comment',
            'has_been_read',
        )

        generic_tasks = Task.objects.filter(verified=False, task_type='generic')
        if self.request.user.is_superuser:
            pass
        elif self.request.user.groups.filter(name='Головной офис').exists():
            generic_tasks = generic_tasks.exclude(executor__is_superuser=True)
        else:
            generic_tasks = generic_tasks.exclude(executor__is_superuser=True).filter(executor=self.request.user)

        generic_tasks = generic_tasks.values(
            'pk',
            'name',
            'executor__first_name',
            'executor__last_name',
            'created_at',
            'planned_completion_date',
            'completed',
            'needs_comment',
            'has_been_read',
        )

        context['tasks'] = list(components_tasks) + list(generic_tasks)
        return context


class TaskUpdateView(UpdateView):
    model = ComponentTask
    form_class = TaskUpdateForm
    template_name = 'tasks/task_update.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """ Если задачу открыл исполнитель, ставим статус - задача прочитана """
        task = self.get_object()
        if request.user == task.executor:
            task.has_been_read = True
            task.save()
        return super().get(request, *args, **kwargs)

    def get_object(self) -> Task:
        if not hasattr(self, '_object'):
            self._object = get_object_or_404(Task, pk=self.kwargs.get('task_pk'))
        return self._object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        context['task'] = task
        context['comment_form'] = TaskCommentForm()
        return context

    def form_valid(self, form):
        task: Task = form.save(commit=False)

        if task.completed and not task.completed_at:
            task.completed_at = timezone.localtime().date()

        if not task.completed:
            task.completed_at = None

        task.save()

        bot_message = f'{self.request.user.get_full_name()} отредактировал задачу {task.name}'
        relative_url = reverse('component_task_update', args=[task.pk])
        full_url = self.request.build_absolute_uri(relative_url)
        bot_message += '\n' + full_url
        notify_telegram(message=bot_message)

        return redirect('tasks')


class TaskCommentCreate(FormView):
    form_class = TaskCommentForm

    def form_valid(self, form):
        task = get_object_or_404(Task, pk=self.kwargs.get('task_pk'))
        task_comment: TaskComment = form.save(commit=False)
        task_comment.task = task
        task_comment.save()

        bot_message = f'{self.request.user.get_full_name()} добавил комментарий к задаче {task.name}'
        bot_message += '\n' + task_comment.text
        relative_url = reverse('component_task_update', args=[task.pk])
        full_url = self.request.build_absolute_uri(relative_url)
        bot_message += '\n' + full_url
        notify_telegram(message=bot_message)

        return redirect(self.request.META.get('HTTP_REFERER', '/'))
