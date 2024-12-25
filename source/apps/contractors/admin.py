from django.contrib import admin

from .models import (Appendix, AppendixAttachment, Contract, ContractAttachment, Contractor, Quotation,
                     QuotationAttachment)


@admin.register(Appendix)
class AppendixAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Appendix._meta.fields]


@admin.register(AppendixAttachment)
class AppendixAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in AppendixAttachment._meta.fields]


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contract._meta.fields]


@admin.register(ContractAttachment)
class ContractAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ContractAttachment._meta.fields]


@admin.register(Contractor)
class ContractorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Contractor._meta.fields]


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Quotation._meta.fields]


@admin.register(QuotationAttachment)
class QuotationAttachmentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in QuotationAttachment._meta.fields]
