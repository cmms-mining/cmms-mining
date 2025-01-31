from django.views.generic import ListView

from apps.documents.models import Document


class DocumentsListView(ListView):
    model = Document
    template_name = 'documents/documents_list.html'
    context_object_name = 'documents'
