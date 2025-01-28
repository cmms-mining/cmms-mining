from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView, View

from .forms import ExcelNomenclatureLoadForm
from .services import load_nomenclature_and_warehouses_to_db, load_running_time_to_db


class ImporterView(TemplateView):
    template_name = 'importer/importer.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['excel_nomenclature_load_form'] = ExcelNomenclatureLoadForm()
        return context


class ExcelNomenclatureLoadView(FormView):
    template_name = 'importer/importer.html'
    form_class = ExcelNomenclatureLoadForm
    success_url = reverse_lazy('importer')

    def form_valid(self, form):
        excel_file: InMemoryUploadedFile = form.cleaned_data['excel_file']
        try:
            load_nomenclature_and_warehouses_to_db(excel_file=excel_file)
            messages.success(self.request, f'Данные из файла {excel_file} загружены!')
        except Exception as e:
            messages.error(self.request, f'Ошибка при обработке файла {excel_file}: {e}')
            return redirect('importer')

        return super().form_valid(form)


class ImportRunningTimeGoogleView(View):
    """Импорт наработки оборудования с гугл таблицы"""

    def get(self, request, *args, **kwargs):
        loaded_running_times = load_running_time_to_db()
        messages.success(self.request, f'Данные по наработки с гугл таблицы загружены:{loaded_running_times}')
        return redirect('importer')
