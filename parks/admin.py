from django.contrib import admin
from parks.models import Park, Zone, ParkingSpot, PriceType

# Register your models here.
admin.site.register(Park)
admin.site.register(Zone)
admin.site.register(ParkingSpot)
admin.site.register(PriceType)
