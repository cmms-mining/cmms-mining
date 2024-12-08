from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import TemplateView

from apps.accounts.forms import LoginForm
from apps.common.bot import notify_telegram


class LoginView(TemplateView):
    template_name = 'accounts/login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        """ Перенаправление на страницу оборудования, если пользователь залогинен """
        if request.user.is_authenticated:
            return redirect('tasks')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')
        password = form.cleaned_data.get('password')
        username = form.cleaned_data.get('username')
        user = authenticate(request, username=username, password=password)
        if not user:
            return redirect('login')
        login(request, user)
        message = f'Зашел {user.get_full_name()}'
        notify_telegram(message=message)
        return redirect('tasks')
