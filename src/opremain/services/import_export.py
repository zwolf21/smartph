from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

from ..models import Narcotic

class NarcoticResource(resources.ModelResource):

    class Meta:
        model = Narcotic
        fields = [
            "narcotic_name", "amt", "company_name", "keyword", "sub_keyword",
            "full_amt_exp", "amt_volum_exp", "amt_weight_exp", "unit"        
        ]
        import_id_fields = "narcotic_name",


class NarcoticImportExportAdmin(ImportExportModelAdmin):
    resource_class = NarcoticResource

