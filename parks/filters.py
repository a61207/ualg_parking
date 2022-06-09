import django_filters
from .models import Park, Zone


class ParkFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', label='Parks')
    address = django_filters.CharFilter(lookup_expr='contains', label='Address')
    postal_code = django_filters.CharFilter(lookup_expr='startswith', label='Postal Code')

    class Meta:
        model = Park
        fields = ['name', 'address', 'postal_code', 'typology']


class ZoneFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='contains', label='Zones')

    class Meta:
        model = Zone
        fields = ['name']
