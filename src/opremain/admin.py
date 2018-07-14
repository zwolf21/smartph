from django.contrib import admin
from .services.import_export import NarcoticImportExportAdmin

from .models import Narcotic, Config, NameMap

@admin.register(Narcotic)
class NarcoticAdmin(NarcoticImportExportAdmin, admin.ModelAdmin):
    list_display = 'narcotic_name', 'company_name', 'amt', 'keyword', 'sub_keyword', 'full_amt_exp', 'amt_volum_exp',
    list_filter = 'company_name', 'unit', 'updated', 'created',
    search_fields = 'narcotic_name',


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = 'title', 'key_column', 'order_amt_column', 'orderby_columns', 'not_null_columns', 'activated',
    list_filter = 'user', 'activated', 'updated', 'created', 


@admin.register(NameMap)
class NameMapAdmin(admin.ModelAdmin):
    list_display = 'current_name', 'mapping_to',
    list_filter = 'config', 'updated', 'created',
    autocomplete_fields = 'mapping_to',