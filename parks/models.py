from django.db import models
from django.utils import timezone
from djmoney.models.fields import MoneyField
from main.models import Administrator

# Create your models here.


class Park(models.Model):
    STRUCTURE = 'ST'
    SURFACE = 'SF'
    TYPOLOGYS = [
        (STRUCTURE, 'Structure'),
        (SURFACE, 'Surface'),
    ]

    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', verbose_name='Name', max_length=50, unique=True)
    address = models.CharField(db_column='Address', verbose_name='Address', max_length=50, unique=True)
    postal_code = models.CharField(db_column='PostalCode', verbose_name='Postal Code', max_length=8, unique=True)
    typology = models.CharField(verbose_name='Typology', db_column='Typology', choices=TYPOLOGYS, max_length=2)
    map_html = models.TextField(db_column='MapLocationHTML', verbose_name='Map Location HTML')
    monday_start = models.TimeField(db_column='MondayStart', verbose_name='Monday Start', null=True)
    monday_end = models.TimeField(db_column='MondayEnd', verbose_name='Monday End', null=True)
    tuesday_start = models.TimeField(db_column='TuesdayStart', verbose_name='Tuesday Start', null=True)
    tuesday_end = models.TimeField(db_column='TuesdayEnd', verbose_name='Tuesday End', null=True)
    wednesday_start = models.TimeField(db_column='WednesdayStart', verbose_name='Wednesday Start', null=True)
    wednesday_end = models.TimeField(db_column='WednesdayEnd', verbose_name='Wednesday End', null=True)
    thursday_start = models.TimeField(db_column='ThursdayStart', verbose_name='Thursday Start', null=True)
    thursday_end = models.TimeField(db_column='ThursdayEnd', verbose_name='Thursday End', null=True)
    friday_start = models.TimeField(db_column='FridayStart', verbose_name='Friday Start', null=True)
    friday_end = models.TimeField(db_column='FridayEnd', verbose_name='Friday End', null=True)
    saturday_start = models.TimeField(db_column='SaturdayStart', verbose_name='Saturday Start', null=True)
    saturday_end = models.TimeField(db_column='SaturdayEnd', verbose_name='Saturday End', null=True)
    sunday_start = models.TimeField(db_column='SundayStart', verbose_name='Sunday Start', null=True)
    sunday_end = models.TimeField(db_column='SundayEnd', verbose_name='Sunday End', null=True)
    is_open = models.BooleanField(verbose_name='IsOpen', db_column='IsOpen', default=False)
    created = models.DateTimeField(db_column='Created', verbose_name='Created', default=timezone.now)
    updated = models.DateTimeField(db_column='Updated', verbose_name='Updated', default=timezone.now)
    admin = models.ForeignKey(Administrator, models.CASCADE, verbose_name='Admin', db_column='Admin',
                              null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/parks/%i/" % self.id

    def map_src(self):
        return self.map_html.split('"')[1]

    def spots(self):
        i = 0
        for zone in self.zones():
            i += zone.spots().count()
        return i

    def zones(self):
        return Zone.objects.filter(park=self.id)


class PriceType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    time = models.DurationField(db_column='TypeTime', verbose_name='Type Time')
    total = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    park = models.ForeignKey(Park, models.CASCADE, db_column='Parque', verbose_name='Park')

    class Meta:
        unique_together = ('time', 'park')


class ContractType(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', verbose_name='Name', max_length=50, unique=True)
    time = models.DurationField(db_column='TypeTime', verbose_name='Type Time')
    total = MoneyField(max_digits=14, decimal_places=2, default_currency='EUR')
    park = models.ForeignKey(Park, models.CASCADE, db_column='Parque', verbose_name='Park')

    class Meta:
        unique_together = ('name', 'park')


class LayoutLine(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    x = models.IntegerField(db_column="Abscissa", verbose_name="Abscissa")
    y = models.IntegerField(db_column="Ordiante", verbose_name="Ordiante")
    w = models.IntegerField(db_column="Width", verbose_name="Width")
    h = models.IntegerField(db_column="Height", verbose_name="Height")


class Zone(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', verbose_name='Name', max_length=50, unique=True)
    park = models.ForeignKey(Park, models.CASCADE, db_column='Parque', verbose_name='Park')

    def spots(self):
        return ParkingSpot.objects.filter(zone=self.id)

    def get_absolute_url(self):
        return "/parks/%i/zones/%i/" % (self.park.id, self.id)


class ParkingSpot(models.Model):
    AVAILABLE = 'AV'
    OCCUPIED = 'OC'
    RESERVED = 'RE'
    STATES = [
        (AVAILABLE, 'Available'),
        (OCCUPIED, 'Occupied'),
        (RESERVED, 'Reserved'),
    ]
    VERTICAL = 'VE'
    HORIZONTAL = 'HO'
    DIRECTIONS = [
        (VERTICAL, 'Vertical'),
        (HORIZONTAL, 'Horizontal'),
    ]
    id = models.AutoField(db_column='ID', primary_key=True)
    number = models.IntegerField(db_column='Number', verbose_name='Number')
    zone = models.ForeignKey(Zone, models.CASCADE, db_column='Zone', verbose_name='Zone')
    state = models.CharField(verbose_name='State', db_column='State', choices=STATES, max_length=2, default=AVAILABLE)
    x = models.IntegerField(db_column="Abscissa", verbose_name="Abscissa")
    y = models.IntegerField(db_column="Ordiante", verbose_name="Ordiante")
    direction = models.CharField(verbose_name='Direction', db_column='Direction', choices=DIRECTIONS, max_length=2)
