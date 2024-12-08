from django.contrib.auth.models import User
from django.db import models


class JobTitle(models.Model):
    """Справочник должностей"""
    name = models.CharField(verbose_name='Название', max_length=100, unique=True)
    site = models.ForeignKey(
        to='sites.Site',
        related_name='job_titles',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Проект',
        )
    work_center = models.ForeignKey(
        to='sites.WorkCenter',
        related_name='job_titles',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Участок',
        )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = '(Справочник) Должности'

    def __str__(self) -> str:
        return self.name


class UserJobTitle(models.Model):
    """Должности пользователей"""
    job_title = models.ForeignKey(
        to='accounts.JobTitle',
        related_name='users_job_titles',
        on_delete=models.CASCADE,
        verbose_name='Должность',
        )
    user = models.OneToOneField(
        verbose_name='Пользователь',
        to=User,
        on_delete=models.CASCADE,
        related_name='user_job_titles',
        )

    class Meta:
        verbose_name = 'Должность пользователя'
        verbose_name_plural = 'Должности пользователей'

    def __str__(self) -> str:
        return self.job_title.name + ' ' + self.user.get_full_name()
