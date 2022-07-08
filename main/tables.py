from django_tables2 import tables, TemplateColumn, Column

from main.models import RoleRequest, Car, Employee


class RoleRequestTable(tables.Table):
    view = TemplateColumn(template_name='tables/role_request_buttons.html', verbose_name="")

    class Meta:
        model = RoleRequest
        fields = ("created", "user__email", "role")


class CarTable(tables.Table):
    view = TemplateColumn(template_name='tables/car_buttons.html', verbose_name="")
    created = Column(verbose_name="Added")

    class Meta:
        model = Car
        fields = ("registration", "foreign", "brand", "model", "created")


class EmployeeTable(tables.Table):
    view = TemplateColumn(template_name='tables/employee_buttons.html', verbose_name="")

    class Meta:
        model = Employee
        fields = ("user__first_name", "user__last_name", "user__email", "user__is_active", "user__date_joined",
                  "user__last_login")


class AdministratorTable(tables.Table):
    view = TemplateColumn(template_name='tables/administrator_buttons.html', verbose_name="")

    class Meta:
        model = Employee
        fields = ("user__first_name", "user__last_name", "user__email", "user__is_active", "user__date_joined",
                  "user__last_login")
