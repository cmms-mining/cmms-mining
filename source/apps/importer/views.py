from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, View

from .forms import ExcelUploadForm
from .google import connect_google_drive
from .services import from_file_to_db


class ImporterView(TemplateView):
    template_name = 'importer/importer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['excel_upload_form'] = ExcelUploadForm()
        return context


class ExcelUploadView(FormView):
    template_name = 'importer/importer.html'
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


class GoogleConnectView(View):

    def get(self, request, *args, **kwargs):
        connect_google_drive()
        messages.success(self.request, 'Подключение успешно!')
        return redirect('importer')
