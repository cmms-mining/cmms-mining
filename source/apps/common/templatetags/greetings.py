from django import template
from django.utils import timezone


register = template.Library()


@register.simple_tag
def get_greeting():
    current_hour = timezone.localtime().hour

    if 5 <= current_hour < 11:
        return 'Доброе утро'
    elif 11 <= current_hour < 17:
        return 'Добрый день'
    elif 17 <= current_hour < 23:
        return 'Добрый вечер'
    else:
        return 'Доброй ночи'
