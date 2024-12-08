from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, FormView, ListView, UpdateView, View

from apps.equipments.forms import RelocationAttachmentForm
from apps.equipments.models import Equipment, EquipmentRelocation, RelocationOrder

from ..forms import (CreateEquipmentRelocationByOrderForm, RelocationOrderAddEquipmentForm, RelocationOrderCreateForm,
                     RelocationOrderUpdateStatusForm)


class RelocationsOrdersListView(ListView):
    model = RelocationOrder
    template_name = 'equipments/orders/orders_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        orders_set = RelocationOrder.objects.prefetch_related(
            Prefetch(
                'equipments',
                queryset=Equipment.objects.prefetch_related(
                    Prefetch(
                        'relocations',
                        queryset=EquipmentRelocation.objects.prefetch_related('attachments'),
                    ),
                ),
            ),
        )

        orders = [
            {
                'instance': order,
                'equipments': [
                    {
                        'instance': equipment,
                        'relocation': {
                            'instance': relocation,
                            'attachments': relocation.attachments.all(),
                        } if (relocation := next(
                            (rel for rel in equipment.relocations.all() if rel.order_id == order.pk),
                            None,
                        )) else None,
                    }
                    for equipment in order.equipments.all()
                ],
            }
            for order in orders_set
        ]

        context['orders'] = orders
        context['user_can_create_relocation'] = self.request.user.groups.filter(name='Перемещение оборудования').exists()

        return context


class RelocationOrderCreateView(CreateView):
    model = RelocationOrder
    form_class = RelocationOrderCreateForm
    template_name = 'equipments/orders/order_create.html'

    def form_valid(self, form):
        order = form.save()
        return redirect('equipment_relocation_order_update', order_pk=order.pk)


class RelocationOrderUpdateView(UpdateView):
    model = RelocationOrder
    context_object_name = 'order'
    form_class = RelocationOrderCreateForm
    template_name = 'equipments/orders/order_update.html'

    def get_object(self):
        return get_object_or_404(RelocationOrder, pk=self.kwargs.get('order_pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['add_equipment_form'] = RelocationOrderAddEquipmentForm()
        context['create_relocation_form'] = CreateEquipmentRelocationByOrderForm()
        context['relocation_attachment_form'] = RelocationAttachmentForm()

        order = self.get_object()
        order_equipments = {}
        for equipment in order.equipments.all():
            order_equipments[equipment.number] = False
            for relocation in equipment.relocations.all():
                if relocation.order == order:
                    order_equipments[equipment.number] = relocation
                    break
        context['order_equipments'] = order_equipments
        context['user_can_create_relocation'] = self.request.user.groups.filter(name='Перемещение оборудования').exists()
        context['order_update_status_form'] = RelocationOrderUpdateStatusForm(initial={'status': order.status})
        return context

    def form_valid(self, form):
        order = form.save()
        return redirect('equipment_relocation_order_update', order_pk=order.pk)


class RelocationOrderAddEquipmentView(FormView):
    form_class = RelocationOrderAddEquipmentForm

    def form_valid(self, form):
        order = get_object_or_404(RelocationOrder, pk=self.kwargs.get('order_pk'))
        equipment = form.cleaned_data['equipment']
        order.equipments.add(equipment)
        return redirect('equipment_relocation_order_update', order_pk=order.pk)


class EquipmentRelocationCreateByOrderView(View):

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(RelocationOrder, pk=kwargs.get('order_pk'))
        for equipment in order.equipments.all():
            EquipmentRelocation.objects.get_or_create(
                equipment=equipment,
                order=order,
                from_site=order.from_site,
                to_site=order.to_site,
            )
        return redirect('equipment_relocation_order_update', order_pk=order.pk)


class RelocationOrderUpdateStatusView(FormView):
    form_class = RelocationOrderUpdateStatusForm

    def form_valid(self, form):
        order = get_object_or_404(RelocationOrder, pk=self.kwargs.get('order_pk'))
        order_status = form.cleaned_data['status']
        order.status = order_status
        order.save()
        return redirect('equipment_relocation_order_update', order_pk=order.pk)
