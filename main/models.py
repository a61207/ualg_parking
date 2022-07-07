from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.utils import timezone


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'User'

    def is_admin(self):
        return Administrator.objects.filter(user=self.id)

    @staticmethod
    def get_absolute_url():
        return "/parks/"

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Administrator(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, db_column='User ID', verbose_name='User')

    class Meta:
        db_table = 'Administrator'
        unique_together = ('id', 'user')

    def __str__(self):
        return self.user.username


class Employee(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, db_column='UserID', verbose_name='User')

    class Meta:
        db_table = 'Employee'
        unique_together = ('id', 'user')

    def get_user(self):
        return self.user.username


class Client(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.OneToOneField(User, models.CASCADE, db_column='UserID', verbose_name='User')
    nif = models.IntegerField(db_column='NIF', verbose_name='NIF', null=True)

    class Meta:
        db_table = 'Client'
        unique_together = ('id', 'user')

    def __str__(self):
        return self.user.username


class Car(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    client = models.ForeignKey(Client, models.CASCADE, db_column='ClientID', verbose_name='Client')
    registration = models.CharField(db_column='Registration', verbose_name='Registration', max_length=8)
    foreign = models.BooleanField(db_column='Is Foreign', verbose_name='Is Foreign')
    brand = models.CharField(db_column='Brand', verbose_name='Brand', max_length=20)
    model = models.CharField(db_column='Model', verbose_name='Model', max_length=20)
    deleted = models.BooleanField(db_column='Deleted', verbose_name='Is Deleted', default=False)
    created = models.DateTimeField(db_column='Created', verbose_name='Created', default=timezone.now)
    updated = models.DateTimeField(db_column='Updated', verbose_name='Updated', default=timezone.now)

    class Meta:
        unique_together = ('registration', 'foreign',)
        db_table = 'Car'

    def __str__(self):
        return self.registration

    def get_absolute_url(self):
        return "/account/%i/cars/" % self.client.user.id


class Notification(models.Model):
    NORMAL = 'NO'
    ROLE_REQUEST = 'RO'
    TYPES = [
        (NORMAL, 'Normal'),
        (ROLE_REQUEST, 'Role Request'),
    ]

    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='UserID', verbose_name='User')
    title = models.CharField(db_column='Title', verbose_name='Title', max_length=30)
    seen = models.BooleanField(db_column='MessageSeen', verbose_name='Message Seen', default=False)
    description = models.TextField(db_column='Description', verbose_name='Description')
    type = models.CharField(verbose_name='Type', db_column='Type', choices=TYPES, max_length=2, default=NORMAL)

    class Meta:
        db_table = 'Notification'


class RoleRequest(models.Model):
    ADMINISTRATOR = 'AD'
    EMPLOYEE = 'EM'
    ROLES = [
        (ADMINISTRATOR, 'Administrator'),
        (EMPLOYEE, 'Employee'),
    ]

    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='UserID', verbose_name='User')
    role = models.CharField(verbose_name='Role', db_column='Role', choices=ROLES, max_length=2)
    is_accepted = models.BooleanField(verbose_name="Is Accepted", db_column='IsAccepted', default=False)
    is_reviewed = models.BooleanField(verbose_name="Is Reviewed", db_column='IsReviewed', default=False)
    is_erased = models.BooleanField(verbose_name="Is Erased", db_column='IsErased', default=False)
    created = models.DateTimeField(db_column='Created', verbose_name='Created', default=timezone.now)
    updated = models.DateTimeField(db_column='Updated', verbose_name='Updated', default=timezone.now)

    class Meta:
        db_table = 'RoleRequest'


class TimePeriod(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    start = models.TimeField(db_column='Start', verbose_name='Start', null=True, blank=True)
    end = models.TimeField(db_column='End', verbose_name='End', null=True, blank=True)

    class Meta:
        db_table = 'TimePeriod'

    def all_day(self):
        return self.start.hour == 0 and self.start.minute == 0 and self.end.hour == 23 and self.end.minute == 59


class DatePeriod(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    start_date = models.DateField(db_column='Start', verbose_name='Start')
    end_date = models.DateField(db_column='End', verbose_name='End')

    class Meta:
        db_table = 'DatePeriod'


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
    city = models.CharField(verbose_name='City', db_column='City', max_length=50)
    typology = models.CharField(verbose_name='Typology', db_column='Typology', choices=TYPOLOGYS, max_length=2)
    map_html = models.TextField(db_column='MapLocationHTML', verbose_name='Map Location HTML')
    is_open = models.BooleanField(verbose_name='Open', db_column='IsOpen', default=False)
    is_archived = models.BooleanField(verbose_name='Archived', db_column='IsArchived', default=False)
    created = models.DateTimeField(db_column='Created', verbose_name='Created', default=timezone.now)
    updated = models.DateTimeField(db_column='Updated', verbose_name='Updated', default=timezone.now)
    admin = models.ForeignKey(Administrator, models.CASCADE, verbose_name='Admin', db_column='Admin',
                              null=True, blank=True)

    class Meta:
        db_table = 'Park'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/parks/%i/" % self.id

    def today_opening_time(self):
        datetime = timezone.now()
        schedule = self.current_weekly_schedule()
        if schedule is None:
            return None
        elif datetime.weekday() == 0:
            return schedule.monday.start
        elif datetime.weekday() == 1:
            return schedule.tuesday.start
        elif datetime.weekday() == 1:
            return schedule.wednesday.start
        elif datetime.weekday() == 1:
            return schedule.thursday.start
        elif datetime.weekday() == 1:
            return schedule.friday.start
        elif datetime.weekday() == 1:
            return schedule.saturday.start
        else:
            return schedule.sunday.start

    def today_closing_time(self):
        schedule = self.current_weekly_schedule()
        if schedule is None:
            result = None
        elif timezone.now().weekday() == 0:
            result = schedule.monday.end
        elif timezone.now().weekday() == 1:
            result = schedule.tuesday.end
        elif timezone.now().weekday() == 1:
            result = schedule.wednesday.end
        elif timezone.now().weekday() == 1:
            result = schedule.thursday.end
        elif timezone.now().weekday() == 1:
            result = schedule.friday.end
        elif timezone.now().weekday() == 1:
            result = schedule.saturday.end
        else:
            result = schedule.sunday.end
        if result.hour == 0 and result.minute == 0:
            result = result.replace(hour=23, minute=59, second=59)
        return result

    def map_src(self):
        return self.map_html.split('"')[1]

    def posta_city(self):
        return self.postal_code + " " + self.city

    def spots(self):
        i = 0
        for zone in self.zones():
            i += zone.spots().count()
        return i

    def free_spots(self, start, end):
        count = 0
        for zone in Zone.objects.filter(park=Park.objects.get(id=self.id)):
            count += zone.free_spots(start, end)
        return count

    def occupied_spots(self, start, end):
        count = 0
        for zone in Zone.objects.filter(park=Park.objects.get(id=self.id)):
            count += zone.occupied_spots(start, end)
        return count

    def reserved_spots(self, start, end):
        count = 0
        for zone in Zone.objects.filter(park=Park.objects.get(id=self.id), is_archived=False):
            count += zone.reserved_spots(start, end)
        return count

    def zones(self):
        return Zone.objects.filter(park=self.id)

    def price_tables(self):
        return PriceTable.objects.filter(park=self.id)

    def current_price_table(self):
        for table in self.price_tables():
            if table.deadline.end_date >= timezone.now().date() >= table.deadline.start_date and \
                    not table.archived:
                return table

    def weekly_schedules(self):
        return WeekSchedule.objects.filter(park=self.id)

    def current_weekly_schedule(self):
        for schedule in self.weekly_schedules():
            if schedule.deadline.end_date >= timezone.now().date() >= schedule.deadline.start_date and \
                    not schedule.archived:
                return schedule

    def non_achived_resources(self):
        return PriceTable.objects.filter(park=self, archived=False).count() + \
               WeekSchedule.objects.filter(park=self, archived=False).count()


class PriceTable(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    deadline = models.OneToOneField(DatePeriod, models.CASCADE, db_column='Deadline', verbose_name='Deadline')
    archived = models.BooleanField(db_column='Archived', verbose_name='Archived', default=False)
    park = models.ForeignKey(Park, models.CASCADE, db_column='Parque', verbose_name='Park')

    def get_prices(self):
        return PriceType.objects.filter(table=self.id)

    def get_n_prices(self):
        return self.get_prices().count()


class PriceType(models.Model):
    NORMAL = 'NO'
    FINE = 'FI'
    TYPE = [
        (NORMAL, 'Normal'),
        (FINE, 'Fine'),
    ]

    id = models.AutoField(db_column='ID', primary_key=True)
    minutes = models.IntegerField(db_column='MinutesTime', verbose_name='Minutes Time', default=0)
    hours = models.IntegerField(db_column='HoursTime', verbose_name='Hours Time', default=0)
    total = models.DecimalField(db_column='TotalValue', verbose_name='Total Value', max_digits=6, decimal_places=2,
                                default=0)
    type = models.CharField(verbose_name='Type', db_column='Type', choices=TYPE, max_length=2)
    table = models.ForeignKey(PriceTable, models.CASCADE, db_column='PriceTable', verbose_name='Price Table')

    class Meta:
        db_table = 'PriceType'
        unique_together = ('minutes', 'hours', 'table', 'type')

    def total_time(self):
        if self.minutes and self.hours:
            return str(self.hours) + "h:" + str(self.minutes) + "m"
        elif self.hours:
            return str(self.hours) + "h"
        else:
            return str(self.minutes) + "m"


class WeekSchedule(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    deadline = models.OneToOneField(DatePeriod, models.CASCADE, db_column='Deadline', verbose_name='Deadline')
    monday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Monday', db_column='Monday',
                                  verbose_name='Monday')
    tuesday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Tuesday', db_column='Tuesday',
                                   verbose_name='Tuesday')
    wednesday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Wednesday', db_column='Wednesday',
                                     verbose_name='Wednesday')
    thursday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Thursday', db_column='Thursday',
                                    verbose_name='Thursday')
    friday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Friday', db_column='Friday',
                                  verbose_name='Friday')
    saturday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Saturday', db_column='Saturday',
                                    verbose_name='Saturday')
    sunday = models.OneToOneField(TimePeriod, models.CASCADE, related_name='Sunday', db_column='Sunday',
                                  verbose_name='Sunday')
    archived = models.BooleanField(db_column='Archived', verbose_name='Archived', default=False)
    park = models.ForeignKey(Park, models.CASCADE, db_column='Parque', verbose_name='Park')

    class Meta:
        db_table = 'WeekSchedule'

    def get_time_days(self):
        queryset = TimePeriod.objects.none()
        queryset |= TimePeriod.objects.filter(id=self.monday.id)
        queryset |= TimePeriod.objects.filter(id=self.tuesday.id)
        queryset |= TimePeriod.objects.filter(id=self.wednesday.id)
        queryset |= TimePeriod.objects.filter(id=self.thursday.id)
        queryset |= TimePeriod.objects.filter(id=self.friday.id)
        queryset |= TimePeriod.objects.filter(id=self.saturday.id)
        queryset |= TimePeriod.objects.filter(id=self.sunday.id)
        return queryset

    def equal_weekend(self):
        return (self.saturday.start is not None and self.saturday.start == self.sunday.start) \
               and (self.saturday.end is not None and self.saturday.end == self.sunday.end)

    def equal_weekdays(self):
        return (self.monday.start is not None and self.monday.start == self.tuesday.start ==
                self.wednesday.start == self.thursday.start == self.friday.start) \
               and (self.monday.end is not None and self.monday.end == self.tuesday.end ==
                    self.wednesday.end == self.thursday.end == self.friday.end)

    def equal_allweek(self):
        return self.equal_weekdays() and self.equal_weekend() and self.monday.start == self.sunday.start \
               and self.monday.end == self.sunday.end

    def occupied_spots(self):
        return Park.objects.get(id=self.park.id).occupied_spots(self.deadline.start_date, self.deadline.end_date)

    def reserved_spots(self):
        return Park.objects.get(id=self.park.id).reserved_spots(self.deadline.start_date, self.deadline.end_date)

    def spots_in_use(self):
        return self.reserved_spots() + self.occupied_spots()


class LayoutLine(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    x = models.IntegerField(db_column="Abscissa", verbose_name="Abscissa")
    y = models.IntegerField(db_column="Ordiante", verbose_name="Ordiante")
    w = models.IntegerField(db_column="Width", verbose_name="Width")
    h = models.IntegerField(db_column="Height", verbose_name="Height")

    class Meta:
        db_table = 'LayoutLine'


class Zone(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name', verbose_name='Name', max_length=50)
    park = models.ForeignKey(Park, models.CASCADE, db_column='ParqueID', verbose_name='Park')
    is_archived = models.BooleanField(verbose_name='Archived', db_column='IsArchived', default=False)
    is_open = models.BooleanField(verbose_name='Open', db_column='IsOpen', default=False)

    class Meta:
        unique_together = ['park', 'name']
        db_table = 'Zone'

    def spots(self):
        return ParkingSpot.objects.filter(zone=self.id)

    def n_spots(self):
        return self.spots().count()

    def free_spots_now(self):
        count = 0
        for spot in ParkingSpot.objects.filter(zone=self.id):
            if spot.get_state(timezone.now().date(), timezone.now().date()) == ParkingSpot.FREE:
                count += 1
        return count

    def free_spots(self, start, end):
        count = 0
        for spot in ParkingSpot.objects.filter(zone=self.id):
            if spot.get_state(start, end) == ParkingSpot.FREE:
                count += 1
        return count

    def occupied_spots(self, start, end):
        count = 0
        for spot in ParkingSpot.objects.filter(zone=self.id):
            if spot.get_state(start, end) == ParkingSpot.OCCUPIED:
                count += 1
        return count

    def reserved_spots(self, start, end):
        count = 0
        for spot in ParkingSpot.objects.filter(zone=self.id, is_archived=False):
            if spot.get_state(start, end) == ParkingSpot.RESERVED:
                count += 1
        return count

    def get_absolute_url(self):
        return "/parks/%i/zones/%i/" % (self.park.id, self.id)


class ParkingSpot(models.Model):
    OCCUPIED = 'OC'
    RESERVED = 'RE'
    FREE = 'FR'
    VERTICAL = 'VE'
    HORIZONTAL = 'HO'
    DIRECTIONS = [
        (VERTICAL, 'Vertical'),
        (HORIZONTAL, 'Horizontal'),
    ]
    id = models.AutoField(db_column='ID', primary_key=True)
    number = models.IntegerField(db_column='NumberID', verbose_name='Number')
    zone = models.ForeignKey(Zone, models.CASCADE, db_column='Zone', verbose_name='Zone')
    x = models.IntegerField(db_column="Abscissa", verbose_name="Abscissa")
    y = models.IntegerField(db_column="Ordiante", verbose_name="Ordiante")
    direction = models.CharField(verbose_name='Direction', db_column='Direction', choices=DIRECTIONS, max_length=2)
    is_archived = models.BooleanField(verbose_name='Archived', db_column='IsArchived', default=False)

    class Meta:
        db_table = 'ParkingSpot'

    def get_state(self, start, end):
        if EntradasSaidas.objects.filter(lugarid=self.id, periocidadeid__start__gte=start,
                                         periocidadeid__end__gte=start) and \
                EntradasSaidas.objects.filter(lugarid=self.id, periocidadeid__start__lte=end,
                                              periocidadeid__end__lte=end):
            return ParkingSpot.OCCUPIED
        elif Reserva.objects.filter(lugarid=self.id, periocidadeid__start__gte=start,
                                    periocidadeid__end__gte=start) and \
                Reserva.objects.filter(lugarid=self.id, periocidadeid__start__lte=end,
                                       periocidadeid__end__lte=end):
            return ParkingSpot.RESERVED
        else:
            return ParkingSpot.FREE


class Estadoreserva(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', unique=True, max_length=15)  # Field name made lowercase.

    class Meta:
        db_table = 'EstadoReserva'


class Modalidadepagamento(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', unique=True, max_length=15)  # Field name made lowercase.

    class Meta:
        db_table = 'ModalidadePagamento'


class Periocidade(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    start = models.DateTimeField(db_column='Start')  # Field name made lowercase.
    end = models.DateTimeField(db_column='End', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'Periocidade'


class Contrato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.CASCADE,
                               db_column='UserID')  # Field name made lowercase.
    lugarid = models.ForeignKey(ParkingSpot, models.DO_NOTHING, db_column='LugarID')
    modalidadepagamentoid = models.ForeignKey(Modalidadepagamento, models.CASCADE,
                                              db_column='ModalidadePagamentoID', blank=True,
                                              null=True)  # Field name made lowercase.
    valorcontrato = models.FloatField(db_column='ValorContrato', blank=True,
                                      null=True)  # Field name made lowercase.
    datainicio = models.DateField(db_column='DataInicio')  # Field name made lowercase.
    datafim = models.DateField(db_column='DataFim', blank=True,
                               null=True)  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=8)  # Field name made lowercase.
    criadoem = models.DateTimeField(db_column='CriadoEm', default=timezone.now)  # Field name made lowercase.
    editadoem = models.DateTimeField(db_column='EditadoEm', default=timezone.now)  # Field name made lowercase.
    estadoreservaid = models.ForeignKey(Estadoreserva, models.DO_NOTHING,
                                        db_column='EstadoReservaID', default=1)

    class Meta:
        db_table = 'Contrato'


class EntradasSaidas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    periocidadeid = models.ForeignKey('Periocidade', models.CASCADE,
                                      db_column='PeriocidadeID')  # Field name made lowercase.
    matriculaviatura = models.ForeignKey(Car, models.CASCADE,
                                         db_column='MatriculaViatura')
    lugarid = models.ForeignKey(ParkingSpot, models.CASCADE, db_column='LugarID')

    class Meta:
        db_table = 'Entradas/Saidas'


class Reserva(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True,
                                   null=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.CASCADE,
                               db_column='UserID')  # Field name made lowercase.
    matricula = models.ForeignKey(Car, models.CASCADE, db_column='matricula',
                                  null=True)  # Field name made lowercase.
    lugarid = models.ForeignKey(ParkingSpot, models.CASCADE, db_column='LugarID')  # Field name made lowercase.
    divida = models.FloatField(db_column='Divida', blank=True, null=True)
    preco = models.FloatField(db_column='Preco', blank=True, null=True)
    periocidadeid = models.ForeignKey(Periocidade, models.CASCADE,
                                      db_column='PeriocidadeID', blank=True,
                                      null=True)  # Field name made lowercase.
    entradassaidasid = models.ForeignKey(EntradasSaidas, models.CASCADE, db_column='entradassaidasID', blank=True,
                                         null=True)
    estadoreservaid = models.ForeignKey(Estadoreserva, models.CASCADE,
                                        db_column='EstadoReservaID', default=1)  # Field name made lowercase.
    criadoem = models.DateTimeField(db_column='CriadoEm', default=timezone.now)  # Field name made lowercase.
    editadoem = models.DateTimeField(db_column='EditadoEm', default=timezone.now)  # Field name made lowercase.

    class Meta:
        db_table = 'Reserva'


class Estadocontrato(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', unique=True, max_length=50)  # Field name made lowercase.

    class Meta:
        db_table = 'EstadoContrato'


class FacturaRecibo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    reservaid = models.ForeignKey('Reserva', models.CASCADE, db_column='ReservaID', blank=True,
                                  null=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True,
                                   null=True)  # Field name made lowercase.
    entradasaidaid = models.ForeignKey(EntradasSaidas, models.CASCADE, db_column='EntradaSaidaID', blank=True,
                                       null=True)  # Field name made lowercase.
    multa = models.TextField(db_column='Multa', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    precores = models.FloatField(db_column='PrecoRes')  # Field name made lowercase.
    emitidaem = models.DateTimeField(db_column='EmitidaEm')  # Field name made lowercase.
    periocidadeid = models.ForeignKey(Periocidade, models.CASCADE,
                                      db_column='PeriocidadeID')  # Field name made lowercase.
    contribuinte = models.TextField(db_column='Contribuinte', null=True)  # Field name made lowercase.
    comprovativopagamento = models.FileField(db_column='Comprovativo')  # Field name made lowercase.
    estadofaturaid = models.ForeignKey(Estadocontrato, models.CASCADE,
                                       db_column='EstadoFaturaID')  # Field name made lowercase.

    class Meta:
        db_table = 'Factura/Recibo'


class Reclamacao(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=100)  # Field name made lowercase.
    email = models.EmailField(db_column='Email', max_length=50)  # Field name made lowercase.
    telefone = models.IntegerField(db_column='Telefone')  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.CASCADE, db_column='ContratoID', blank=True,
                                   null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descrição', max_length=30)

    class Meta:
        db_table = 'Reclamacao'
