from django import forms


class ExcelNomenclatureLoadForm(forms.Form):
    excel_file = forms.FileField(label="Загрузить Excel файл")
