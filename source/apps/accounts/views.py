from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.common.bot import notify_telegram


class LoginView(TemplateView):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        """ Перенаправление на страницу оборудования, если пользователь залогинен """
        if request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password', '').strip()
        username = request.POST.get('username', '').strip()
        user = authenticate(request, username=username, password=password)
        if not user:
            return redirect('login')
        login(request, user)
        message = f'Зашел {user.get_full_name()}'
        notify_telegram(message=message)
        return redirect('tasks')
