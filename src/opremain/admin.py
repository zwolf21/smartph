from django.contrib import admin
from .services.import_export import NarcoticImportExportAdmin

from .models import Narcotic, Config, NameMap, NarcoticUseFile

@admin.register(Narcotic)
class NarcoticAdmin(NarcoticImportExportAdmin, admin.ModelAdmin):
    list_display = 'narcotic_name', 'keyword', 'company_keyword', 'amt_ml', 'amt_mg', 'sub_keyword', 'full_amt_exp', 'amt_volum_exp',
    list_filter = 'company_keyword', 'unit', 'narcotic_class', 'shape', 'updated', 'created',
    search_fields = 'narcotic_name',


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    list_display = 'title', 'user', 'key_column', 'order_amt_column', 'orderby_columns', 'not_null_columns', 'activated',
    list_filter = 'user', 'activated', 'updated', 'created', 


@admin.register(NameMap)
class NameMapAdmin(admin.ModelAdmin):
    list_display = 'config', 'current_name', 'mapping_to', 'excepted', 'activated',
    list_filter = 'excepted', 'config', 'updated', 'created', 'activated',
    autocomplete_fields = 'mapping_to',


@admin.register(NarcoticUseFile)
class NarcoticUseFileAdmin(admin.ModelAdmin):
    list_display = 'description', 'created', 'updated',
    list_filter = 'created',