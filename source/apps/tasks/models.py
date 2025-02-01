from django.contrib.auth.models import User
from django.db import models

from apps.common.services import get_user


class Task(models.Model):
    """Задачи"""
    TASK_TYPE_CHOICES = (
        ('generic', 'Обычная задача'),
        ('component', 'Задача компонента'),
    )
    task_type = models.CharField(
        verbose_name='Тип задачи',
        max_length=20,
        choices=TASK_TYPE_CHOICES,
        default='generic',
    )
    name = models.CharField(verbose_name='Название', max_length=100)
    executor = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='tasks_assigned',
        verbose_name='Исполнитель',
        )
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, verbose_name='Инициатор', on_delete=models.CASCADE, related_name='authored_tasks')
    planned_completion_date = models.DateField(verbose_name='Плановая дата выполнения', blank=True, null=True)
    completed_at = models.DateField(verbose_name='Дата выполнения', blank=True, null=True)
    completed = models.BooleanField(verbose_name='Выполнено', default=False)
    updated_by = models.ForeignKey(
        verbose_name='Последний редактор',
        to=User,
        on_delete=models.CASCADE,
        related_name='tasks_last_edited',
        null=True,
        )
    updated_at = models.DateTimeField(verbose_name='Дата редактирования', auto_now=True, null=True)
    verified = models.BooleanField(verbose_name='Проверено', default=False)
    has_been_read = models.BooleanField(verbose_name='Прочитана исполнителем', default=False)
    needs_comment = models.BooleanField(verbose_name='Требуется комментарий', default=False)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        user = get_user()
        if not self.pk:
            self.author = user
        self.updated_by = user
        super().save(*args, **kwargs)

    def is_edit_allowed(self) -> bool:
        """Доступность к редактированию"""
        if self.verified:
            return False
        return True

    def __str__(self) -> str:
        return self.name


class TaskComment(models.Model):
    task = models.ForeignKey(to='tasks.Task', verbose_name='Задача', on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        to=User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='authored_tasks_comments',
        blank=True,
        )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий задачи'
        verbose_name_plural = 'Комментарии задач'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if not self.pk:
            self.author = get_user()
        super(TaskComment, self).save(*args, **kwargs)

    def __str__(self):
        return self.text
