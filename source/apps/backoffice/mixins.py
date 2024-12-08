from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import Http404


class SuperuserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404()
