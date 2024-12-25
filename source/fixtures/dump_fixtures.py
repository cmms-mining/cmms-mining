import json
import os
import sys
from io import StringIO

import django

# Добавляем директорию на уровень выше в `sys.path`
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.core.management import call_command


MODEL_ORDER = [
    'auth.Group',
    'auth.User',

    'accounts.CustomGroup',
    'accounts.JobTitle',
    'accounts.UserJobTitle',

    'tasks.Task',
    'tasks.TaskComment',

    'sites.WorkCenter',
    'sites.Site',

    'common.TechStateOption',

    'equipments.EquipmentType',
    'equipments.EquipmentModel',
    'equipments.Equipment',
    'equipments.CharacteristicGroup',
    'equipments.CharacteristicValue',
    'equipments.Characteristic',
    'equipments.RelocationOrder',
    'equipments.EquipmentRelocation',
    'equipments.RelocationAttachment',
    'equipments.EquipmentCurrentData',
    'equipments.Nameplate',

    'components.ComponentKind',
    'components.ComponentType',
    'components.ComponentInstallationLocation',
    'components.Component',
    'components.ComponentState',
    'components.ComponentTechState',
    'components.ComponentTask',
    'components.ComponentRepair',
    'components.ComponentRelocation',
    'components.ComponentReconciliation',
    'components.ComponentInstallation',
    'components.ComponentDeinstallation',
    'components.ComponentTypeEquipmentModel',
    'components.ComponentCurrentData',
    'components.ComponentAttachment',

    'contractors.Contractor',
    'contractors.Contract',
    'contractors.ContractAttachment',
    'contractors.Appendix',
    'contractors.AppendixAttachment',
    'contractors.Quotation',
    'contractors.QuotationAttachment',
]

# Получаем директорию, где находится сам скрипт
script_dir = os.path.dirname(os.path.abspath(__file__))

output_file = os.path.join(script_dir, "fixtures.json")

all_data = []

# Открываем файл для записи данных
with open(output_file, "w") as f:
    for model_path in MODEL_ORDER:
        app_label, model_name = model_path.rsplit('.', 1)

        # Создаём объект StringIO для захвата вывода команды dumpdata
        out = StringIO()

        # Выгружаем данные модели в StringIO (stdout)
        print(f'Выгружаем данные для {model_path}...')
        call_command('dumpdata', f'{app_label}.{model_name}', indent=2, stdout=out)

        # Получаем строку из StringIO и загружаем её в формате JSON
        model_data = json.loads(out.getvalue())

        all_data.extend(model_data)

    json.dump(all_data, f, indent=2)

print('Выгрузка завершена')
