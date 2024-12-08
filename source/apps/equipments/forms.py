from django import forms

from apps.equipments.models import Equipment, EquipmentRelocation, RelocationAttachment, RelocationOrder
# from apps.sites.models import Site


class EquipmentRelocationForm(forms.ModelForm):
    class Meta:
        model = EquipmentRelocation
        fields = ('from_site', 'to_site', 'date', 'order', 'note')
        widgets = {
            'from_site': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'to_site': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'order': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 300px; height: 70px;'}),
        }

    # def __init__(self, *args, **kwargs):
    #     site_instance = kwargs.pop('site_instance', None)
    #     super().__init__(*args, **kwargs)

    #     # Если есть объект site_instance, задаем значение для поля from_site
    #     if site_instance:
    #         self.fields['from_site'].initial = site_instance
    #         self.fields['from_site'].widget.attrs['disabled'] = True
    #         # Добавляем скрытое поле, чтобы отправить значение 'from_site'
    #         self.fields['from_site_hidden'] = forms.CharField(widget=forms.HiddenInput(), initial=site_instance)

    #         self.fields['to_site'].queryset = Site.objects.exclude(pk=site_instance.pk)

    # def clean(self):
    #     cleaned_data = super().clean()
    #     # Устанавливаем значение from_site из скрытого поля
    #     if cleaned_data.get('from_site_hidden'):
    #         from_site = Site.objects.get(name=cleaned_data.get('from_site_hidden'))
    #         cleaned_data['from_site'] = from_site
    #     return cleaned_data


class RelocationOrderCreateForm(forms.ModelForm):

    class Meta:
        model = RelocationOrder
        fields = ('number', 'date', 'from_site', 'to_site', 'scan')
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 120px;'}),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'from_site': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'to_site': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'scan': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        }


class RelocationOrderAddEquipmentForm(forms.Form):
    equipment = forms.ModelChoiceField(
        queryset=Equipment.objects.all(),
        label='Оборудование',
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 270px;'}),
    )


class RelocationOrderUpdateStatusForm(forms.Form):
    status = forms.ChoiceField(
        label='Статус',
        choices=RelocationOrder.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 270px;'}),
    )


class CreateEquipmentRelocationByOrderForm(forms.Form):
    pass


class RelocationAttachmentForm(forms.ModelForm):

    class Meta:
        model = RelocationAttachment
        fields = ('attachment_file',)
        widgets = {
            'attachment_file': forms.FileInput(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
        }
