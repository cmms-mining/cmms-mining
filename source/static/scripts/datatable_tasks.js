// https://datatables.net/extensions/fixedheader/examples/integration/columnFiltering.html

$(document).ready(function() {
    // Устанавливаем момент для сортировки дат в формате 'DD/MM/YYYY'
    $.fn.dataTable.moment('DD.MM.YYYY');

    new DataTable('#tasks_table', {
        paging: false,
        order: [[0, 'desc']], // Сортировка по первому столбцу по возрастанию
        initComplete: function () {
            this.api()
                .columns()
                .every(function () {
                    let column = this;
                    let title = column.footer().textContent;
    
                    // Create input element
                    let input = document.createElement('input');
                    input.placeholder = title;
                    column.footer().replaceChildren(input);
    
                    // Event listener for user input
                    input.addEventListener('keyup', () => {
                        if (column.search() !== this.value) {
                            column.search(input.value).draw();
                        }
                    });
                });
        },
        fixedHeader: {
            footer: true
        },
        language: {
            url: '//cdn.datatables.net/plug-ins/2.1.5/i18n/ru.json',
        },
    });
});