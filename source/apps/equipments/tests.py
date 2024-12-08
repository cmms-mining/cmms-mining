from django.contrib.auth.models import User
from django.test import Client, TestCase, override_settings
from django.urls import reverse

from apps.equipments.models import Equipment, EquipmentModel, EquipmentType

from maintenance.models import MaintenanceCategory


@override_settings(AXES_ENABLED=False)
class TestEquipmentView(TestCase):

    def setUp(self):
        test_user = User.objects.create(
            username='test_user_name',
        )
        test_user.set_password('testpass')
        test_user.save()
        self.client_anonim = Client()
        self.client_login = Client()
        self.client_login.login(username='test_user_name', password='testpass')
        self.equipment_type = EquipmentType.objects.create(name='test_type', slug='test_type')
        self.equipment_model = EquipmentModel.objects.create(name='test_model', equipment_type=self.equipment_type)
        self.equipment = Equipment.objects.create(number='test_number', equipment_model=self.equipment_model)

        self.maintenance_category = MaintenanceCategory.objects.create(name='test_maintenance_category')

        return super().setUp()

    def test_equipment_types_list(self):
        """test EquipmentTypesListView"""
        response = self.client_anonim.get(reverse('equipment_types'))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('equipment_types'))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment_types.html')

    def test_equipment_models_list(self):
        """test EquipmentModelsListView"""
        response = self.client_anonim.get(reverse('equipment_models', args=[self.equipment_type.slug]))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('equipment_models', args=[self.equipment_type.slug]))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment_models.html')

    def test_equipments_listl(self):
        """test EquipmentsListView"""
        response = self.client_anonim.get(reverse('equipments_list',
                                                  args=[self.equipment_type.slug, self.equipment_model.name],
                                                  ))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('equipments_list',
                                                 args=[self.equipment_type.slug, self.equipment_model.name],
                                                 ))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipments_list.html')

    def test_equipment_detail(self):
        """test EquipmentDetailView"""
        response = self.client_anonim.get(reverse('equipment_detail',
                                                  args=[
                                                    self.equipment_type.slug,
                                                    self.equipment_model.name,
                                                    self.equipment.number,
                                                    ],
                                                  ))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('equipment_detail',
                                                 args=[
                                                   self.equipment_type.slug,
                                                   self.equipment_model.name,
                                                   self.equipment.number,
                                                   ],
                                                 ))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/equipment_detail.html')

    def test_equipment_maintenance(self):
        """test EquipmentMaintenanceView"""
        response = self.client_anonim.get(reverse('equipment_maintenance',
                                                  args=[
                                                    self.equipment_type.slug,
                                                    self.equipment_model.name,
                                                    self.equipment.number,
                                                    ],
                                                  ))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('equipment_maintenance',
                                                 args=[
                                                   self.equipment_type.slug,
                                                   self.equipment_model.name,
                                                   self.equipment.number,
                                                   ],
                                                 ))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/equipment_maintenance.html')

    def test_equipment_attachment(self):
        """test EquipmentAttachmentView"""
        response = self.client_anonim.get(reverse('equipment_attachment',
                                                  args=[
                                                    self.equipment_type.slug,
                                                    self.equipment_model.name,
                                                    self.equipment.number,
                                                    ],
                                                  ))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('equipment_attachment',
                                                 args=[
                                                   self.equipment_type.slug,
                                                   self.equipment_model.name,
                                                   self.equipment.number,
                                                   ],
                                                 ))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipment/equipment_attachment.html')

    def test_maintenance_card(self):
        """test MaintenanceCardView"""
        response = self.client_anonim.get(reverse('maintenance_card',
                                                  args=[
                                                    self.equipment_type.slug,
                                                    self.equipment_model.name,
                                                    self.equipment.number,
                                                    self.maintenance_category.name,
                                                    ],
                                                  ))
        self.assertAlmostEquals(response.status_code, 302)
        self.assertRedirects(response, '/')

        response = self.client_login.get(reverse('maintenance_card',
                                                 args=[
                                                   self.equipment_type.slug,
                                                   self.equipment_model.name,
                                                   self.equipment.number,
                                                   self.maintenance_category.name,
                                                   ],
                                                 ))
        self.assertAlmostEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'maintenance_card.html')
