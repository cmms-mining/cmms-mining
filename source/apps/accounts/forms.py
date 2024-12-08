from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(required=False, label='Логин', widget=forms.TextInput(
                               attrs={
                                    'class': 'form-control form-control-lg',
                                    'placeholder': 'Логин',
                                    'autocomplete': 'off',
                                }))
    password = forms.CharField(required=False, label='Пароль', strip=False, widget=forms.PasswordInput(
                                attrs={
                                    'class': 'form-control form-control-lg',
                                    'placeholder': 'Пароль',
                                    'autocomplete': 'off',
                                }))
