from django.contrib import admin
from main.models import *

# Register your models here.

# noinspection DuplicatedCode
admin.site.register(User)
admin.site.register(Administrator)
admin.site.register(Client)
admin.site.register(Employee)
admin.site.register(Car)
admin.site.register(Notification)
admin.site.register(RoleRequest)
admin.site.register(Park)
admin.site.register(Zone)
# noinspection DuplicatedCode
admin.site.register(ParkingSpot)
# noinspection DuplicatedCodes
admin.site.register(WeekSchedule)
admin.site.register(TimePeriod)
admin.site.register(PriceType)
admin.site.register(Estadoreserva)
admin.site.register(Reserva)
admin.site.register(Contrato)
admin.site.register(FacturaRecibo)
admin.site.register(Estadocontrato)
admin.site.register(Periocidade)
admin.site.register(Modalidadepagamento)
admin.site.register(EntradasSaidas)
