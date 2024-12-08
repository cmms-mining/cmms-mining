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
