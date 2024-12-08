from django.db import models

from apps.common.models import Relocation


class BucketRelocation(Relocation):
    """Перемещение ковшей"""
    bucket = models.ForeignKey(
        to='buckets.Bucket',
        related_name='relocations',
        on_delete=models.CASCADE,
        verbose_name='Ковш',
    )

    class Meta:
        verbose_name = 'Перемещение ковша'
        verbose_name_plural = 'Перемещения ковшей'
        ordering = ['-date']

    def is_edit_allowed(self) -> bool:
        """Доступность к редактированию (только последнее перемещение ковша)"""
        bucket = self.bucket
        if int(self.pk) == int(BucketRelocation.objects.filter(bucket=bucket).first().pk):
            return True
        return False

    def __str__(self):
        return self.bucket.number + ' из ' + self.from_site.name + ' в ' + \
               self.to_site.name + ' ' + self.date.strftime("%d-%m-%Y")


def attach_buck_reloc_upload_path(instance, filename):
    # Генерируем путь сохранения файла, используя имя оборудования и имя файла
    return f'buckets/{instance.bucket_relocation.bucket.number}/relocations' \
           f'/{instance.bucket_relocation.date.strftime("%d-%m-%Y")}/{filename}'


class BucketRelocationAttachment(models.Model):
    attachment_file = models.FileField(upload_to=attach_buck_reloc_upload_path, verbose_name='Файл вложения')
    bucket_relocation = models.ForeignKey(
        to='buckets.BucketRelocation',
        related_name='attachments',
        on_delete=models.CASCADE,
        verbose_name='Перемещение ковша',
    )
    description = models.CharField(verbose_name='Описание', max_length=150, blank=True, null=True)

    class Meta:
        verbose_name = 'Вложение перемещения ковша'
        verbose_name_plural = 'Вложения перемещения ковшей'

    def __str__(self):
        return f'Вложение перемещение ковша {self.bucket_relocation.bucket.number}'
