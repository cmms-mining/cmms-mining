from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ExcelUploadForm
from .services import from_file_to_db


class ExcelUploadView(FormView):
    template_name = 'importer/upload_excel.html'
    form_class = ExcelUploadForm
    success_url = reverse_lazy('importer')

    def form_valid(self, form):
        excel_file = form.cleaned_data['excel_file']
        try:
            from_file_to_db(excel_file=excel_file)
            messages.success(self.request, 'Данные успешно загружены!')
        except Exception as e:
            messages.error(self.request, f'Ошибка при обработке файла: {e}')
            return redirect('importer')

        return super().form_valid(form)
