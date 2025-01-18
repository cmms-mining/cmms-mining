from django import forms

from .models import FirefightingCheck


class FirefightingCheckCreateForm(forms.ModelForm):

    class Meta:
        model = FirefightingCheck
        fields = ('date', 'attachment_file', 'state', 'note')
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'state': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'attachment_file': forms.ClearableFileInput(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'note': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 500px;'}),
        }
