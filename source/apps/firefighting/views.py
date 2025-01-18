from django.views.generic import ListView

from .models import FirefightingSystem


class FirefightingsListView(ListView):
    context_object_name = 'firefighting_systems'
    template_name = 'firefighting/firefightings_list.html'
    model = FirefightingSystem
