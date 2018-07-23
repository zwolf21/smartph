from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from import_export.admin import ImportExportModelAdmin

from ..models import Narcotic

class NarcoticResource(resources.ModelResource):

    class Meta:
        model = Narcotic
        fields = [
            "narcotic_name","keyword","sub_keyword","company_keyword","full_amt_exp","amt_volum_exp","amt_weight_exp","pct_exp",
            "amt_ml","amt_mg","edi_code","price","narcotic_class","shape", "unit"
        ]
        import_id_fields = "narcotic_name",


class NarcoticImportExportAdmin(ImportExportModelAdmin):
    resource_class = NarcoticResource
