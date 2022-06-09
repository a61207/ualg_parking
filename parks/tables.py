from django_tables2 import tables, TemplateColumn, Column

from parks.models import Park


class ParkTable(tables.Table):
    view = TemplateColumn(template_name='tables/park_buttons.html', verbose_name="")

    class Meta:
        model = Park
        fields = ("name", "address", "postal_code", "typology")


class ZoneTable(tables.Table):
    view = TemplateColumn(template_name='tables/zone_buttons.html', verbose_name="")
    n_spots = Column(verbose_name='Spots')
    n_available_spots = Column(verbose_name='Available')

    class Meta:
        model = Park
        fields = ("name", "n_spots", "n_available_spots")
