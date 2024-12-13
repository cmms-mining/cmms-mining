from django.urls import path

from .views import components, installations, reconciliations, relocations, repairs, tasks, techstates


urlpatterns = [
    path('', components.ComponentsListView.as_view(), name='components'),
    path(
        '<slug:component_number>/state',
        components.ComponentStateView.as_view(),
        name='component_state_tab',
        ),

    # Установки компонентов
    path(
        '<slug:component_number>/installations',
        installations.ComponentInstallationsTabView.as_view(),
        name='component_installations_tab',
        ),
    path(
        '<slug:component_number>/deinstallation/create',
        installations.ComponentDeinstallationCreateView.as_view(),
        name='component_deinstallation_create',
        ),
    path(
        '<slug:component_number>/installation/create',
        installations.ComponentInstallationCreateView.as_view(),
        name='component_installation_create',
        ),

    # Техсостояния компонентов
    path(
        '<slug:component_number>/techstates',
        techstates.ComponentTechStatesListView.as_view(),
        name='component_techstates_tab',
        ),
    path(
        '<slug:component_number>/techstate/create',
        techstates.ComponentTechStatesCreateView.as_view(),
        name='component_techstate_create',
        ),

    # Перемещения компонентов
    path(
        '<slug:component_number>/relocations',
        relocations.ComponentRelocationsTabView.as_view(),
        name='component_relocations_tab',
        ),
    path(
        '<slug:component_number>/relocation/create',
        relocations.ComponentRelocationCreateView.as_view(),
        name='component_relocation_create',
        ),

    # Задачи компонентов
    path(
        '<slug:component_number>/tasks',
        tasks.ComponentTasksListView.as_view(),
        name='component_tasks_tab',
        ),
    path(
        '<slug:component_number>/task/create',
        tasks.ComponentTaskCreateView.as_view(),
        name='component_task_create',
        ),
    path(
        'task/<int:task_pk>/update',
        tasks.ComponentTaskUpdateView.as_view(),
        name='component_task_update',
        ),

    # Сверки компонентов
    path(
        '<slug:component_number>/reconciliations',
        reconciliations.ComponentReconciliationsTabView.as_view(),
        name='component_reconciliations_tab',
        ),

    # Ремонты компонентов
    path(
        'repairs',
        repairs.ComponentsRepairsListView.as_view(),
        name='components_repairs',
        ),

]
