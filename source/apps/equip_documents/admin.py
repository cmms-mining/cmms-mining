from django.contrib import admin

from apps.equip_documents.models import DocumentType, EquipmentDocument


@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in DocumentType._meta.fields]


@admin.register(EquipmentDocument)
class EquipmentDocumentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in EquipmentDocument._meta.fields]
