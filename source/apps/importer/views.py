from django.contrib import messages
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
        from_file_to_db(excel_file=excel_file)
        messages.success(self.request, "Данные успешно загружены!")

        # try:
        #     # Чтение Excel-файла с помощью pandas
        #     df = pd.read_excel(excel_file)

        #     # Проверка структуры данных
        #     expected_columns = ['column1', 'column2', 'column3']
        #     if not all(col in df.columns for col in expected_columns):
        #         messages.error(self.request, "Некорректный формат файла.")
        #         return super().form_invalid(form)

        #     # Загрузка данных в базу
        #     for _, row in df.iterrows():
        #         ExcelData.objects.create(
        #             column1=row['column1'],
        #             column2=row['column2'],
        #             column3=row['column3'],
        #         )

        #     messages.success(self.request, "Данные успешно загружены!")
        # except Exception as e:
        #     messages.error(self.request, f"Ошибка при обработке файла: {e}")
        #     return super().form_invalid(form)

        return super().form_valid(form)
