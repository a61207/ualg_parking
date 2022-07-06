import django_filters

from main.models import RoleRequest, Car, Employee


class RoleRequestFilter(django_filters.FilterSet):
    user = django_filters.CharFilter(lookup_expr='contains', label='User')

    class Meta:
        model = RoleRequest
        fields = ['user', ]


class EmployeeFilter(django_filters.FilterSet):
    user__first_name = django_filters.CharFilter(lookup_expr='contains', label='First Name')
    user__last_name = django_filters.CharFilter(lookup_expr='contains', label='Last Name')
    user__email = django_filters.CharFilter(lookup_expr='contains', label='Email')

    class Meta:
        model = Employee
        fields = ['user__first_name', 'user__last_name', 'user__email', 'user__is_active']


class CarFilter(django_filters.FilterSet):
    registration = django_filters.CharFilter(lookup_expr='contains', label='Registration')
    brand = django_filters.CharFilter(lookup_expr='contains', label='Brand')
    model = django_filters.CharFilter(lookup_expr='contains', label='Model')

    class Meta:
        model = Car
        fields = ['registration', 'foreign', 'brand', 'model']
