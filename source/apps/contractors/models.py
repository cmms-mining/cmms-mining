from django.db import models

from apps.common.services import set_file_size, validate_scan_file


class Contractor(models.Model):
    """Контрагенты"""
    name = models.CharField(verbose_name='Наименование', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Подрядчик'
        verbose_name_plural = 'Подрядчики'
        ordering = ['name']

    def __str__(self):
        return self.name


class Contract(models.Model):
    """Контракты с подрядчиками"""
    number = models.CharField(verbose_name='Номер', max_length=200)
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    contractor = models.ForeignKey(
        to='contractors.Contractor',
        on_delete=models.CASCADE,
        related_name='contracts',
        verbose_name='Контрагент',
        )
    description = models.CharField(verbose_name='Описание', max_length=200, blank=True, null=True)
    components = models.ManyToManyField(
        to='components.Component',
        related_name='contracts',
        verbose_name='Компоненты',
        blank=True,
    )

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'
        ordering = ['date']

    def __str__(self):
        return f'Контракт с {self.contractor.name} {self.number} от {self.date}'


def contract_attachment_upload_path(instance, filename):
    return f'contracts/{instance.contract.contractor.name}' \
           f'/{instance.contract.number}_{instance.contract.date.strftime("%Y%m%d")}/{filename}'


class ContractAttachment(models.Model):
    """Файлы вложений для контрактов"""
    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=contract_attachment_upload_path,
        validators=[validate_scan_file],
    )
    contract = models.ForeignKey(
        to='contractors.Contract',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Контракт',
        )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение контракта'
        verbose_name_plural = 'Вложения контрактов'

    def save(self, *args, **kwargs):
        set_file_size(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вложение контракта {self.contract.number} c {self.contract.contractor.name}'


class Appendix(models.Model):
    """Приложения к контрактам"""
    number = models.CharField(verbose_name='Номер', max_length=200)
    date = models.DateField(verbose_name='Дата', blank=True, null=True)
    contract = models.ForeignKey(
        to='contractors.Contract',
        on_delete=models.CASCADE,
        related_name='appendixes',
        verbose_name='Контракт',
        )
    note = models.CharField(verbose_name='Примечание', max_length=200, blank=True, null=True)
    components = models.ManyToManyField(
        to='components.Component',
        related_name='appendixes',
        verbose_name='Компоненты',
        blank=True,
    )

    class Meta:
        verbose_name = 'Приложение к контракту'
        verbose_name_plural = 'Приложения к контрактам'
        ordering = ['date']
        constraints = [models.UniqueConstraint(fields=['contract', 'number'], name='unique_appendix_contract')]

    def __str__(self):
        return f'Приложение {self.number} к контракту с {self.contract.contractor.name} {self.contract.number}'


def appendix_attachment_upload_path(instance, filename):
    return f'contracts/{instance.appendix.contract.contractor.name}' \
           f'/{instance.appendix.contract.number}_{instance.appendix.contract.date.strftime("%Y%m%d")}' \
           f'/{instance.appendix.number}/{filename}'


class AppendixAttachment(models.Model):
    """Файлы вложений для контрактов"""
    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=appendix_attachment_upload_path,
        validators=[validate_scan_file],
    )
    appendix = models.ForeignKey(
        to='contractors.Appendix',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='Приложение',
        )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение для приложения к контракту'
        verbose_name_plural = 'Вложения для приложений к контрактам'

    def save(self, *args, **kwargs):
        set_file_size(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вложение приложения {self.appendix.number} к контракту {self.appendix.contract.number}'


class Quotation(models.Model):
    """Коммерческие предложения от контрагентов"""
    number = models.CharField(verbose_name='Номер', max_length=200, blank=True, null=True)
    date = models.DateField(verbose_name='Дата')
    contractor = models.ForeignKey(
        to='contractors.Contractor',
        on_delete=models.CASCADE,
        related_name='quotations',
        verbose_name='Контрагент',
        )
    description = models.CharField(verbose_name='Описание', max_length=200, unique=True)
    components = models.ManyToManyField(
        to='components.Component',
        related_name='quotations',
        verbose_name='Компоненты',
        blank=True,
    )

    class Meta:
        verbose_name = 'Коммерческое предложение'
        verbose_name_plural = 'Коммерческие предложения'
        ordering = ['date']

    def __str__(self):
        return f'КП от {self.contractor.name} от {self.date.strftime("%d-%m-%Y")}'


def quotation_attachment_upload_path(instance, filename):
    return f'quotations/{instance.quotation.contractor.name}' \
           f'/{instance.quotation.date.strftime("%Y%m%d")}/{filename}'


class QuotationAttachment(models.Model):
    """Файлы вложений для коммерческих предложений"""
    attachment_file = models.FileField(
        verbose_name='Файл',
        upload_to=quotation_attachment_upload_path,
        validators=[validate_scan_file],
    )
    quotation = models.ForeignKey(
        to='contractors.Quotation',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name='КП',
        )
    file_size = models.CharField(verbose_name='Размер файла', max_length=30, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение для КП'
        verbose_name_plural = 'Вложения для КП'

    def save(self, *args, **kwargs):
        set_file_size(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Вложение для КП от {self.quotation.contractor.name}' \
               f'от {self.quotation.date.strftime("%d-%m-%Y")}'
