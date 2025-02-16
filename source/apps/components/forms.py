from django import forms

from apps.common.services import get_user
from apps.components.models import (Component, ComponentDeinstallation, ComponentInstallation,
                                    ComponentRelocation, ComponentRepair, ComponentState, ComponentTask,
                                    ComponentTechState)
from apps.equipments.models import Equipment
from apps.sites.models import Site
from apps.tasks.models import TaskComment


class ComponentDeinstallationForm(forms.ModelForm):
    class Meta:
        model = ComponentDeinstallation
        fields = ('date', 'reason', 'note')
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'reason': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 70px;'}),
        }


class ComponentInstallationForm(forms.ModelForm):

    class Meta:
        model = ComponentInstallation
        fields = ('to_equipment', 'location', 'date', 'note')
        labels = {
            'to_equipment': 'Оборудование',
        }
        widgets = {
            'to_equipment': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'location': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 70px;'}),
        }

    def __init__(self, *args, **kwargs):
        component: Component = kwargs.pop('component', None)
        super(ComponentInstallationForm, self).__init__(*args, **kwargs)

        # Фильтрация queryset для поля 'to_equipment'
        equipment_models = component.get_compatible_equipment_models()
        equipments = Equipment.objects.filter(equipment_model__in=equipment_models)
        self.fields['to_equipment'].queryset = equipments

        # Костыль - фильтрация для получения мест установки компонента
        # неверно брать первое по счету оборудование из списка equipments
        # т.к. на разных моделях оборудования компонент может ставиться в разных местах
        # например цилиндр домкрата - где-то три, где-то четыре
        equipment: Equipment = equipments.first()

        # если компонент устанавливается не один на оборудование (насосы, цилиндры парные)
        if equipment and equipment.equipment_model.get_component_install_locations_number(component=component) > 1:
            locations = component.get_compatible_installation_locations()
            self.fields['location'].queryset = locations
            self.fields['location'].required = True
        else:
            self.fields.pop('location', None)


class ComponentTechStateForm(forms.ModelForm):
    is_operable = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Подлежит эксплуатации',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )

    class Meta:
        model = ComponentTechState
        fields = ('date', 'techstate', 'is_operable', 'description')
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'techstate': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 300px; height: 70px;'}),
        }


class ComponentRelocationForm(forms.ModelForm):
    class Meta:
        model = ComponentRelocation
        fields = ('from_site', 'to_site', 'date', 'note')
        widgets = {
            'from_site': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'to_site': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 70px;'}),
        }

    def __init__(self, *args, **kwargs):
        site_instance = kwargs.pop('site_instance', None)
        super().__init__(*args, **kwargs)

        # Если есть объект site_instance, задаем значение для поля from_site
        if site_instance:
            self.fields['from_site'].initial = site_instance
            self.fields['from_site'].widget.attrs['disabled'] = True
            # Добавляем скрытое поле, чтобы отправить значение 'from_site'
            self.fields['from_site_hidden'] = forms.CharField(widget=forms.HiddenInput(), initial=site_instance)

            self.fields['to_site'].queryset = Site.objects.exclude(pk=site_instance.pk)

    def clean(self):
        cleaned_data = super().clean()
        # Устанавливаем значение from_site из скрытого поля
        if cleaned_data.get('from_site_hidden'):
            from_site = Site.objects.get(name=cleaned_data.get('from_site_hidden'))
            cleaned_data['from_site'] = from_site
        return cleaned_data


class ComponentTaskCreateForm(forms.ModelForm):

    class Meta:
        model = ComponentTask
        fields = ('name', 'executor', 'planned_completion_date')
        widgets = {
            'name': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 300px; height: 70px;'}),
            'executor': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'planned_completion_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
        }


class ComponentTaskUpdateForm(forms.ModelForm):
    completed = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Задача выполнена',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 100px;'}),
        )

    class Meta:
        model = ComponentTask
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


class ComponentStateForm(forms.Form):
    state = forms.ModelChoiceField(
        queryset=ComponentState.objects.all(),
        label='Состояние',
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 270px;'}),
    )
    is_serial_number_marked = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Нанесен серийный номер',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 70px;'}),
        )
    nomenclature_code = forms.CharField(
        label='Код номенклатуры',
        max_length=25,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 270px;'}),
    )
    serial_number = forms.CharField(
        label='Серийный номер',
        max_length=25,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 270px;'}),
    )
    requires_action = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Требует действия',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 70px;'}),
        )
    note = forms.CharField(
        label='Примечание',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 70px;'}),
    )


class ComponentTaskCommentForm(forms.ModelForm):

    class Meta:
        model = TaskComment
        fields = ('text',)
        labels = {
            'text': 'Добавьте комментарий при необходимости',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 700px; height: 150px;'}),
        }


class ComponentRepairForm(forms.ModelForm):

    class Meta:
        model = ComponentRepair
        fields = ('worklist', 'plan_end_date', 'priority', 'note', 'completed_at')
        widgets = {
            'worklist': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 50px;'}),
            'plan_end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 200px;'},
                ),
            'priority': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 200px;'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 50px;'}),
            'completed_at': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 200px;'},
                ),
        }
