from django_tables2 import tables, TemplateColumn, Column

from main.models import RoleRequest, Car, Employee


class RoleRequestTable(tables.Table):
    view = TemplateColumn(template_name='tables/role_request_buttons.html', verbose_name="")

    class Meta:
        model = RoleRequest
        fields = ("created", "user", "role")


class CarTable(tables.Table):
    view = TemplateColumn(template_name='tables/car_buttons.html', verbose_name="")

    class Meta:
        model = Car
        fields = ("registration", "foreign", "brand", "model")


class EmployeeTable(tables.Table):

    class Meta:
        model = Employee
        fields = ("user__get_full_name", "user__email", "user__is_active")
