from django import forms

from apps.contractors.models import Appendix


class AppendixCreateForm(forms.ModelForm):

    class Meta:
        model = Appendix
        fields = ('number', 'date', 'contract', 'note')
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'style': 'max-width: 120px;'}),
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'class': 'form-control', 'type': 'date', 'style': 'max-width: 300px;'},
                ),
            'contract': forms.Select(attrs={'class': 'form-control', 'style': 'max-width: 300px;'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'style': 'max-width: 300px; height: 70px;'}),
        }
