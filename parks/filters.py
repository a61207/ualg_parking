import django_filters
from django import forms

from main.models import Park, Zone, WeekSchedule, PriceTable


class ParkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', label='Parks')
    address = django_filters.CharFilter(lookup_expr='contains', label='Address')
    city = django_filters.CharFilter(lookup_expr='contains', label='City')
    typology = django_filters.ChoiceFilter(choices=Park.TYPOLOGYS, empty_label="All")
    is_archived = django_filters.BooleanFilter()

    class Meta:
        model = Park
        fields = ['name', 'address', 'city', 'typology', 'is_open', 'is_archived']


# noinspection DuplicatedCode
class WeekScheduleFilter(django_filters.FilterSet):
    deadline__start_date = django_filters.DateFilter(lookup_expr='gte', label='Min Start',
                                                     widget=forms.DateInput(attrs={'type': 'date'}))
    deadline__end_date = django_filters.DateFilter(lookup_expr='lte', label='Max End',
                                                   widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = WeekSchedule
        fields = ('deadline__start_date', 'deadline__end_date', 'archived')


# noinspection DuplicatedCode
class PriceTableFilter(django_filters.FilterSet):
    deadline__start_date = django_filters.DateFilter(lookup_expr='gte', label='Min Start',
                                                     widget=forms.DateInput(attrs={'type': 'date'}))
    deadline__end_date = django_filters.DateFilter(lookup_expr='lte', label='Max End',
                                                   widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = PriceTable
        fields = ('deadline__start_date', 'deadline__end_date', 'archived')


class ZoneFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', label='Zones')

    class Meta:
        model = Zone
        fields = ['name', 'is_open', 'is_archived']
