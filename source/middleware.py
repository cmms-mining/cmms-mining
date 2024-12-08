import logging

from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone


class LoginRequiredMiddleware:

    def __init__(self, get_response):
        self.db_logger = logging.getLogger('db')
        self.get_response = get_response

    def __call__(self, request: WSGIRequest):
        if not request.user.is_authenticated and request.path != reverse('login'):
            ip_address = self.get_client_ip(request)
            self.db_logger.info(
                f'{timezone.localtime()}-{request.path_info}-{request.environ.get("HTTP_X_REAL_IP")}-{ip_address}',
                  )
            return redirect(reverse('login'))
        response = self.get_response(request)
        return response

        # Метод для получения IP-адреса клиента
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # Берем первый IP в цепочке
        else:
            ip = request.META.get('REMOTE_ADDR')  # Если заголовка X-Forwarded-For нет
        return ip
