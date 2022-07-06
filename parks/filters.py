import django_filters
from django import forms

from main.models import Park, Zone, WeekSchedule


class ParkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', label='Parks')
    address = django_filters.CharFilter(lookup_expr='contains', label='Address')
    city = django_filters.CharFilter(lookup_expr='contains', label='City')

    class Meta:
        model = Park
        fields = ['name', 'address', 'city', 'typology']


class WeekScheduleFilter(django_filters.FilterSet):
    deadline__start_date = django_filters.DateFilter(lookup_expr='gt', label='Min Start',
                                                     widget=forms.DateInput(attrs={'type': 'date'}))
    deadline__end_date = django_filters.DateFilter(lookup_expr='lt', label='Max End',
                                                   widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = WeekSchedule
        fields = ('deadline__start_date', 'deadline__end_date', 'arquived')


class ZoneFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', label='Zones')

    class Meta:
        model = Zone
        fields = ['name']