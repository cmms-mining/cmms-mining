def set_file_size(instance):
    """ Расчет и запись размера файла в модель (instance) """
    if instance.attachment_file:
        file_size = instance.attachment_file.size // 1048576
        if file_size > 0:
            instance.file_size = str(file_size) + ' мБ'
        else:
            file_size = instance.attachment_file.size // 1024
            instance.file_size = str(file_size) + ' кБ'
