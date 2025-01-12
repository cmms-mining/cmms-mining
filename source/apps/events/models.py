def get_eventfile_upload_path(instance, filename):
    # Генерируем путь сохранения файла, используя дату события
    return f'events/{instance.event.equipment.number}/{instance.event.date}/{instance.event.pk}/{filename}'
