from django import forms
from django.shortcuts import get_object_or_404

from apps.buckets.models import (
                        Bucket, BucketDeinstallation, BucketInstallation, BucketReconciliation, BucketRelocation,
                        BucketRelocationAttachment, BucketRepair, BucketTechState, ToothAdapter,
                    )
from apps.common.models import TechStateOption
from apps.equipments.models import Equipment
from apps.sites.models import Site


class BucketRelocationForm(forms.ModelForm):
    class Meta:
        model = BucketRelocation
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


class BucketRelocationAttachmentForm(forms.ModelForm):
    class Meta:
        model = BucketRelocationAttachment
        fields = ('attachment_file', 'description')


class BucketTechStateForm(forms.ModelForm):
    is_operable = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Подлежит эксплуатации',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )

    class Meta:
        model = BucketTechState
        fields = ('date', 'techstate', 'is_operable', 'description')
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'techstate': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 300px; height: 70px;'}),
        }


class BucketReconciliationForm(forms.ModelForm):
    location = forms.ModelChoiceField(
        queryset=Site.objects.all(),
        label='Местоположение',
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.none(),
        label='Оборудование',
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        required=False,
        )
    adapter = forms.ModelChoiceField(
        queryset=ToothAdapter.objects.all(),
        label='Тип адаптера',
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )
    techstate = forms.ModelChoiceField(
        queryset=TechStateOption.objects.all(),
        label='Техсостояние',
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )
    is_being_repaired = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='В ремонте',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )
    is_operable = forms.ChoiceField(
        choices=[(True, 'ДА'), (False, 'НЕТ')],
        label='Подлежит эксплуатации',
        required=True,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        )

    class Meta:
        model = BucketReconciliation
        fields = ()

    # Передаем объект bucket в kwargs формы
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        kwargs['bucket'] = bucket
        return kwargs

    def __init__(self, *args, **kwargs):
        bucket = kwargs.pop('bucket', None)
        super(BucketReconciliationForm, self).__init__(*args, **kwargs)
        # Фильтрация queryset для поля 'to_equipment'
        self.fields['equipment'].queryset = Equipment.objects.filter(
                equipment_model=bucket.equipment_model,
            )


class BucketDeinstallationForm(forms.ModelForm):
    class Meta:
        model = BucketDeinstallation
        fields = ('date', 'reason', 'note')
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'reason': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 70px;'}),
        }


class BucketInstallationForm(forms.ModelForm):
    class Meta:
        model = BucketInstallation
        fields = ('to_equipment', 'date', 'note')
        labels = {
            'to_equipment': 'Оборудование',
        }
        widgets = {
            'to_equipment': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 500px; height: 70px;'}),
        }

    def __init__(self, *args, **kwargs):
        bucket = kwargs.pop('bucket', None)
        super(BucketInstallationForm, self).__init__(*args, **kwargs)
        # Фильтрация queryset для поля 'to_equipment'
        self.fields['to_equipment'].queryset = Equipment.objects.filter(
                equipment_model=bucket.equipment_model,
            )


class BucketRepairForm(forms.ModelForm):
    class Meta:
        model = BucketRepair
        fields = ('plan_start_date', 'start_date', 'plan_end_date', 'end_date', 'worklist', 'note')
        widgets = {
            'start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'plan_start_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'plan_end_date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'worklist': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 1000px; height: 100px;'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 1000px; height: 70px;'}),
        }

    def __init__(self, *args, **kwargs):
        plan_start_date = kwargs.pop('plan_start_date', None)
        plan_end_date = kwargs.pop('plan_end_date', None)
        start_date = kwargs.pop('start_date', None)
        end_date = kwargs.pop('end_date', None)
        super().__init__(*args, **kwargs)

        if plan_start_date:
            self.fields['plan_start_date'].initial = plan_start_date
            self.fields['plan_start_date'].widget.attrs['disabled'] = True
            self.fields['plan_start_date_hidden'] = forms.CharField(widget=forms.HiddenInput(), initial=plan_start_date)
        if plan_end_date:
            self.fields['plan_end_date'].initial = plan_end_date
            self.fields['plan_end_date'].widget.attrs['disabled'] = True
            self.fields['plan_end_date_hidden'] = forms.CharField(widget=forms.HiddenInput(), initial=plan_end_date)
        if start_date:
            self.fields['start_date'].initial = start_date
            self.fields['start_date'].widget.attrs['disabled'] = True
            self.fields['start_date_hidden'] = forms.CharField(widget=forms.HiddenInput(), initial=start_date)
        if end_date:
            self.fields['end_date'].initial = end_date
            self.fields['end_date'].widget.attrs['disabled'] = True
            self.fields['end_date_hidden'] = forms.CharField(widget=forms.HiddenInput(), initial=end_date)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('plan_start_date_hidden'):
            cleaned_data['plan_start_date'] = cleaned_data.get('plan_start_date_hidden')
        if cleaned_data.get('plan_end_date_hidden'):
            cleaned_data['plan_end_date'] = cleaned_data.get('plan_end_date_hidden')
        if cleaned_data.get('start_date_hidden'):
            cleaned_data['start_date'] = cleaned_data.get('start_date_hidden')
        if cleaned_data.get('end_date_hidden'):
            cleaned_data['end_date'] = cleaned_data.get('end_date_hidden')
        return cleaned_data
