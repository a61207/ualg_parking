from django.contrib import admin

# Register your models here.
from reserves.models import Estadoreserva, Reserva, Contrato, FacturaRecibo, Estadocontrato, Modalidadepagamento, \
    Periocidade, EntradasSaidas

admin.site.register(Estadoreserva)
admin.site.register(Reserva)
admin.site.register(Contrato)
admin.site.register(FacturaRecibo)
admin.site.register(Estadocontrato)
admin.site.register(Periocidade)
admin.site.register(Modalidadepagamento)
admin.site.register(EntradasSaidas)
