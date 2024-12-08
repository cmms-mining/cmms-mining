document.addEventListener('DOMContentLoaded', function () {
    // Получаем все input с type="file" на странице
    const fileInputs = document.querySelectorAll('input[type="file"]');

    fileInputs.forEach(function (fileInput) {
        const id = fileInput.id.split('-')[2]; // Извлекаем уникальный идентификатор (pk)
        const fileNameSpan = document.getElementById('file-name-' + id);
        const submitButton = document.getElementById('submit-btn-' + id);

        fileInput.addEventListener('change', function () {
            if (this.files.length > 0) {
                // Отображаем имя выбранного файла
                fileNameSpan.textContent = this.files[0].name;

                // Показываем кнопку "Загрузить"
                submitButton.classList.remove('d-none');
            } else {
                // Сбрасываем в исходное состояние
                fileNameSpan.textContent = 'Файл не выбран';
                submitButton.classList.add('d-none');
            }
        });
    });
});
