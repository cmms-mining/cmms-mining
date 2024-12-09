from django import forms

from apps.common.services import get_user
from apps.tasks.models import Task, TaskComment


class TaskUpdateForm(forms.ModelForm):
    completed = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Задача выполнена',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 100px;'}),
        )

    class Meta:
        model = Task
        fields = ('planned_completion_date', 'completed')
        widgets = {
            'planned_completion_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = get_user()
        if user and user.is_superuser:
            self.fields['needs_comment'] = forms.ChoiceField(
                choices=[(True, 'ДА'), (False, 'НЕТ')],
                label='Требует комментария',
                widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 100px;'}),
            )
            self._meta.fields += ('needs_comment',)

            self.fields['verified'] = forms.ChoiceField(
                choices=[(True, 'ДА'), (False, 'НЕТ')],
                label='Проверено',
                widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 100px;'}),
            )
            self._meta.fields += ('verified',)

            self.fields['priority'] = forms.ChoiceField(
                choices=Task.PRIORITY_CHOICES,
                label='Приоритет',
                widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 150px;'}),
            )
            self._meta.fields += ('priority',)


class TaskCommentForm(forms.ModelForm):

    class Meta:
        model = TaskComment
        fields = ('text',)
        labels = {
            'text': 'Добавьте комментарий при необходимости',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 700px; height: 150px;'}),
        }
