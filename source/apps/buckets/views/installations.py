from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, View

from apps.buckets.forms import BucketDeinstallationForm, BucketInstallationForm
from apps.buckets.models import Bucket, BucketDeinstallation, BucketInstallation
from apps.buckets.services import get_combined_installs_and_deinstalls
from apps.equipments.models import Equipment


class FormValidationMixin:
    def validate_form(self, form):
        de_installation = self.de_installation
        bucket: Bucket = self.de_installation.bucket

        if isinstance(self, BucketDeinstallationCreateView):
            if not bucket.get_equipment():
                messages.warning(self.request, 'Ковш не установлен на оборудовании!')
                return False

            last_installation_date = bucket.get_installation().date
            if de_installation.date <= last_installation_date:
                messages.warning(
                    self.request,
                    'Ошибка - дата демонтажа ковша не может быть меньше или равна дате предыдущей установки!',
                    )
                return False

        if isinstance(self, BucketInstallationCreateView):
            equipment: Equipment = self.de_installation.to_equipment

            if equipment.is_bucket_installed():
                messages.warning(
                    self.request,
                    f'Ошибка - на {equipment.number} экскаваторе уже установлен '
                    f'<a href=\'{reverse("bucket_all_events_tab", args=[equipment.get_bucket().number])}\''
                    f'target="_blank">ковш {equipment.get_bucket().number}</a>',
                    )
                return False

            if bucket.get_equipment():
                messages.warning(self.request, 'Ковш уже установлен на оборудовании!')
                return False

            if bucket.get_installation() and de_installation.date <= bucket.get_installation().date:
                messages.warning(
                    self.request,
                    'Дата установки ковша не может быть меньше или равна дате предыдущего демонтажа!',
                    )
                return False

            if bucket.get_is_being_repaired():
                messages.warning(
                    self.request,
                    'Установка находящегося в ремонте ковша невозможна!',
                    )
                return False

        if de_installation.date > timezone.localtime().date():
            messages.warning(
                self.request,
                'Ошибка - дата не может быть больше текущей!',
                )
            return False

        return True


class BucketInstallationsTabView(TemplateView):
    template_name = 'buckets/installations/bucket_installations_tab.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket

        comb_installations = get_combined_installs_and_deinstalls(bucket=bucket)
        context['comb_installations'] = comb_installations

        context['installations_tab'] = True
        return context


class BucketDeinstallationCreateView(FormValidationMixin, CreateView):
    model = BucketDeinstallation
    form_class = BucketDeinstallationForm
    template_name = 'buckets/installations/bucket_deinstallation_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        context['installations_tab'] = True
        return context

    def form_valid(self, form):
        deinstallation: BucketDeinstallation = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        deinstallation.bucket = bucket
        self.de_installation = deinstallation

        if not self.validate_form(form):
            return redirect('bucket_installations_tab', bucket_number=bucket.number)

        deinstallation.from_equipment = bucket.get_equipment()
        deinstallation.author = self.request.user
        deinstallation.save()
        messages.success(self.request, 'Ковш демонтирован. Обновите техсостояние при необходимости!')
        return redirect('bucket_installations_tab', bucket_number=bucket.number)


class BucketInstallationCreateView(FormValidationMixin, CreateView):
    model = BucketDeinstallation
    form_class = BucketInstallationForm
    template_name = 'buckets/installations/bucket_installation_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        context['bucket'] = bucket
        context['installations_tab'] = True
        return context

    def form_valid(self, form):
        installation: BucketInstallation = form.save(commit=False)
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        installation.bucket = bucket

        self.de_installation = installation

        if not self.validate_form(form):
            return redirect('bucket_installations_tab', bucket_number=bucket.number)

        installation.author = self.request.user
        installation.save()
        messages.success(self.request, 'Ковш установлен!')
        return redirect('bucket_installations_tab', bucket_number=bucket.number)

    # Передаем объект bucket в kwargs формы
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        bucket = get_object_or_404(Bucket, number=self.kwargs.get('bucket_number'))
        kwargs['bucket'] = bucket
        return kwargs


class BucketDeinstallationDeleteView(View):

    def post(self, request, pk, *args, **kwargs):
        bucket_deinstallation = get_object_or_404(BucketDeinstallation, pk=pk)
        bucket_deinstallation.delete()
        messages.warning(self.request, 'Запись о демонтаже ковша удалена!')
        return redirect('bucket_installations_tab', bucket_number=bucket_deinstallation.bucket.number)


class BucketInstallationDeleteView(View):

    def post(self, request, pk, *args, **kwargs):
        bucket_installation = get_object_or_404(BucketInstallation, pk=pk)
        bucket_installation.delete()
        messages.warning(self.request, 'Запись об установке ковша удалена!')
        return redirect('bucket_installations_tab', bucket_number=bucket_installation.bucket.number)
