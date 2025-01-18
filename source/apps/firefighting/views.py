from django.views.generic import TemplateView


class FirefightingsListView(TemplateView):
    template_name = 'firefighting/firefightings_list.html'
