def get_user():
    from django.contrib.auth.models import AnonymousUser
    import inspect
    for frame_record in inspect.stack():
        if frame_record[3] == 'get_response':
            user = frame_record[0].f_locals['request'].user
            if isinstance(user, AnonymousUser):
                user = None
            break
        else:
            user = None
    return user


def validate_scan_file(value):
    from django.core.exceptions import ValidationError
    if not value.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
        raise ValidationError('Допустимы только файлы PDF, JPG или PNG.')


def set_file_size(instance):
    """ Расчет и запись размера файла в модель (instance) """
    if instance.attachment_file:
        file_size = instance.attachment_file.size // 1048576
        if file_size > 0:
            instance.file_size = str(file_size) + ' мБ'
        else:
            file_size = instance.attachment_file.size // 1024
            instance.file_size = str(file_size) + ' кБ'
