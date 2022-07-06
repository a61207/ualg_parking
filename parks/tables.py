from django.utils.html import format_html
from django_tables2 import tables, TemplateColumn, Column

from main.models import Park, WeekSchedule


class ParkTable(tables.Table):
    view = TemplateColumn(template_name='tables/park_buttons.html', verbose_name="")

    class Meta:
        model = Park
        fields = ("name", "address", "posta_city", "typology")


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
                  "saturday", "sunday", "arquived")

    @staticmethod
    def render_monday(record):
        if record.monday.start is None:
            return format_html("Closed")
        elif record.monday.start == record.monday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.monday.start, record.monday.end)

    @staticmethod
    def render_tuesday(record):
        if record.tuesday.start is None:
            return format_html("Closed")
        elif record.tuesday.start == record.tuesday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.tuesday.start, record.tuesday.end)

    @staticmethod
    def render_wednesday(record):
        if record.wednesday.start is None:
            return format_html("Closed")
        elif record.wednesday.start == record.wednesday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.wednesday.start, record.wednesday.end)

    @staticmethod
    def render_thursday(record):
        if record.thursday.start is None:
            return format_html("Closed")
        elif record.thursday.start == record.thursday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.thursday.start, record.thursday.end)

    @staticmethod
    def render_friday(record):
        if record.friday.start is None:
            return format_html("Closed")
        elif record.friday.start == record.friday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.friday.start, record.friday.end)

    @staticmethod
    def render_saturday(record):
        if record.saturday.start is None:
            return format_html("Closed")
        elif record.saturday.start == record.saturday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.saturday.start, record.saturday.end)

    @staticmethod
    def render_sunday(record):
        if record.sunday.start is None:
            return format_html("Closed")
        elif record.sunday.start == record.sunday.end:
            return format_html("All Day")
        return format_html("{} to {}", record.sunday.start, record.sunday.end)


class ZoneTable(tables.Table):
    view = TemplateColumn(template_name='tables/zone_buttons.html', verbose_name="")
    n_spots = Column(verbose_name='Spots')
    free_spots_now = Column(verbose_name='Available')

    class Meta:
        model = Park
        fields = ("name", "n_spots", "free_spots_now")
