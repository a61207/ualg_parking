from django_tables2 import tables, TemplateColumn, A

from parks.models import Park


class ParkTable(tables.Table):
    view = TemplateColumn(template_name='tables/park_buttons.html')

    class Meta:
        model = Park
        fields = ("name", "address", "postal_code", "typology")


class ZoneTable(tables.Table):
    view = TemplateColumn(template_name='tables/zone_buttons.html')

    class Meta:
        model = Park
        fields = ("name",)
