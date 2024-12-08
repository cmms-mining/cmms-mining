from datetime import datetime

from django import template
from django.utils import timezone


register = template.Library()


@register.filter
def days_from(target_date) -> int | str:
    if target_date:
        if target_date == datetime(1999, 1, 1).date():
            return 'XX'
        today = timezone.localtime().date()
        delta = (today - target_date).days
        return delta if delta > 0 else 1
