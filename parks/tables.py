from django.utils.html import format_html
from django_tables2 import tables, TemplateColumn, Column

from main.models import Park, WeekSchedule, PriceTable, Zone


class ParkTable(tables.Table):
    view = TemplateColumn(template_name='tables/park_buttons.html', verbose_name="")
    postal_code = Column(verbose_name="Postal Code")

    class Meta:
        model = Park
        fields = ("name", "address", "postal_code", "typology", "is_open", "is_archived")

    @staticmethod
    def render_postal_code(record):
        return record.posta_city()


class ClientParkTable(tables.Table):
    view = TemplateColumn(template_name='tables/park_buttons.html', verbose_name="")
    postal_code = Column(verbose_name="Postal Code")

    class Meta:
        model = Park
        fields = ("name", "address", "postal_code", "typology", "is_open")

    @staticmethod
    def render_postal_code(record):
        return record.posta_city()


class WeekScheduleTable(tables.Table):
    monday = Column()
    tuesday = Column()
    wednesday = Column()
    thursday = Column()
    friday = Column()
    saturday = Column()
    sunday = Column()
    view = TemplateColumn(template_name='tables/schedule_buttons.html', verbose_name="")

    class Meta:
        model = WeekSchedule
        fields = ("deadline.start_date", "deadline.end_date", "monday", "tuesday", "wednesday", "thursday", "friday",
                  "saturday", "sunday", "archived")

    @staticmethod
    def render_monday(record):
        if record.monday.start is None:
            return format_html("Closed")
        elif record.monday.all_day():
            return format_html("All Day")
        return format_html("{}:{} to {}:{}", record.monday.start.hour, record.monday.start.minute,
                           record.monday.end.hour, record.monday.end.minute)

    @staticmethod
    def render_tuesday(record):
        if record.tuesday.start is None:
            return format_html("Closed")
        elif record.tuesday.all_day():
            return format_html("All Day")
        return format_html("{}:{} to {}:{}", record.monday.start.hour, record.monday.start.minute,
                           record.monday.end.hour, record.monday.end.minute)

    @staticmethod
    def render_wednesday(record):
        if record.wednesday.start is None:
            return format_html("Closed")
        elif record.wednesday.all_day():
            return format_html("All Day")
        return format_html("{}:{} to {}:{}", record.wednesday.start.hour, record.wednesday.start.minute,
                           record.wednesday.end.hour, record.wednesday.end.minute)

    @staticmethod
    def render_thursday(record):
        if record.thursday.start is None:
            return format_html("Closed")
        elif record.thursday.all_day():
            return format_html("All Day")
        return format_html("{}:{} to {}:{}", record.thursday.start.hour, record.thursday.start.minute,
                           record.thursday.end.hour, record.thursday.end.minute)

    @staticmethod
    def render_friday(record):
        if record.friday.start is None:
            return format_html("Closed")
        elif record.friday.all_day():
            return format_html("All Day")
        return format_html("{}:{} to {}:{}", record.friday.start.hour, record.friday.start.minute,
                           record.friday.end.hour, record.friday.end.minute)

    @staticmethod
    def render_saturday(record):
        if record.saturday.start is None:
            return format_html("Closed")
        elif record.saturday.all_day():
            return format_html("All Day")
        return format_html("{} to {}", record.saturday.start.hour, record.saturday.start.minute,
                           record.saturday.end.hour, record.saturday.end.minute)

    @staticmethod
    def render_sunday(record):
        if record.sunday.start is None:
            return format_html("Closed")
        elif record.sunday.all_day():
            return format_html("All Day")
        return format_html("{}:{} to {}:{}", record.sunday.start.hour, record.sunday.start.minute,
                           record.sunday.end.hour, record.sunday.end.minute)


class PriceTableTable(tables.Table):
    view = TemplateColumn(template_name='tables/price_buttons.html', verbose_name="")
    get_n_prices = Column(verbose_name='Prices')

    class Meta:
        model = PriceTable
        fields = ("deadline.start_date", "deadline.end_date", "get_n_prices", "archived")


class ZoneTable(tables.Table):
    view = TemplateColumn(template_name='tables/zone_buttons.html', verbose_name="")

    class Meta:
        model = Zone
        fields = ("name", "is_open", "is_archived")


class ClientZoneTable(tables.Table):
    view = TemplateColumn(template_name='tables/zone_buttons.html', verbose_name="")
    n_spots = Column(verbose_name='Spots')
    free_spots_now = Column(verbose_name='Available')

    class Meta:
        model = Zone
        fields = ("name", "n_spots", "free_spots_now", "is_open")


class OccupancySpotTable(tables.Table):
    n_spots = Column(verbose_name='Spots')
    free_spots_now = Column(verbose_name='Available')

    class Meta:
        model = Zone
        fields = ("name", "n_spots", "free_spots_now", "is_open")
