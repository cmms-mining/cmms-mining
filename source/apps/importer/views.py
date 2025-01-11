from django.views.generic import TemplateView


class ExcelImportView(TemplateView):
    template_name = 'importer/excel_import.html'
