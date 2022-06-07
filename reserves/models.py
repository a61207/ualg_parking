from django.db import models

# Create your models here.
from django.utils import timezone

from main.models import User, Car
from parks.models import Park, Zone, ParkingSpot


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
    userid = models.ForeignKey(User, models.DO_NOTHING,
                               db_column='UserID')  # Field name made lowercase.
    parqueid = models.ForeignKey(Park, models.DO_NOTHING, db_column='ParqueID')
    zonaid = models.ForeignKey(Zone, models.CASCADE, db_column='ZonaID')  # Field name made lowercase.
    modalidadepagamentoid = models.ForeignKey(Modalidadepagamento, models.DO_NOTHING,
                                              db_column='ModalidadePagamentoID')  # Field name made lowercase.
    datavalidade = models.DateField(db_column='DataValidade')  # Field name made lowercase.
    valorcontrato = models.FloatField(db_column='ValorContrato')  # Field name made lowercase.
    datainicio = models.DateField(db_column='DataInicio')  # Field name made lowercase.
    matricula = models.CharField(db_column='Matricula', max_length=8)  # Field name made lowercase.
    criadoem = models.DateTimeField(db_column='CriadoEm')  # Field name made lowercase.
    editadoem = models.DateTimeField(db_column='EditadoEm')  # Field name made lowercase.

    class Meta:
        db_table = 'Contrato'


class EntradasSaidas(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    periocidadeid = models.ForeignKey('Periocidade', models.DO_NOTHING,
                                      db_column='PeriocidadeID')  # Field name made lowercase.
    matriculaviatura = models.ForeignKey(Car, models.DO_NOTHING,
                                         db_column='MatriculaViatura')  # Field name made lowercase.

    class Meta:
        db_table = 'Entradas/Saidas'


class Reserva(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parqueid = models.ForeignKey(Park, models.DO_NOTHING, db_column='ParqueID')
    contratoid = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='ContratoID', blank=True,
                                   null=True)  # Field name made lowercase.
    userid = models.ForeignKey(User, models.DO_NOTHING,
                               db_column='UserID')  # Field name made lowercase.
    matricula = models.ForeignKey(Car, models.DO_NOTHING, db_column='matricula',
                                  null=True)  # Field name made lowercase.
    lugarid = models.ForeignKey(ParkingSpot, models.DO_NOTHING, db_column='LugarID')  # Field name made lowercase.
    divida = models.FloatField(db_column='Divida', blank=True, null=True)
    preco = models.FloatField(db_column='Preco', blank=True, null=True)
    periocidadeid = models.ForeignKey(Periocidade, models.DO_NOTHING,
                                      db_column='PeriocidadeID', blank=True,
                                      null=True)  # Field name made lowercase.
    entradassaidasid = models.ForeignKey(EntradasSaidas, models.DO_NOTHING, db_column='entradassaidasID', blank=True,
                                         null=True)
    estadoreservaid = models.ForeignKey(Estadoreserva, models.DO_NOTHING,
                                        db_column='EstadoReservaID')  # Field name made lowercase.
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
    reservaid = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='ReservaID', blank=True,
                                  null=True)  # Field name made lowercase.
    contratoid = models.ForeignKey(Contrato, models.DO_NOTHING, db_column='ContratoID', blank=True,
                                   null=True)  # Field name made lowercase.
    entradasaidaid = models.ForeignKey(EntradasSaidas, models.DO_NOTHING, db_column='EntradaSaidaID', blank=True,
                                       null=True)  # Field name made lowercase.
    multa = models.TextField(db_column='Multa', blank=True,
                             null=True)  # Field name made lowercase. This field type is a guess.
    precores = models.FloatField(db_column='PrecoRes')  # Field name made lowercase.
    emitidaem = models.DateTimeField(db_column='EmitidaEm')  # Field name made lowercase.
    periocidadeid = models.ForeignKey(Periocidade, models.DO_NOTHING,
                                      db_column='PeriocidadeID')  # Field name made lowercase.
    contribuinte = models.TextField(db_column='Contribuinte', null=True)  # Field name made lowercase.
    comprovativopagamento = models.FileField(db_column='Comprovativo')  # Field name made lowercase.
    estadofaturaid = models.ForeignKey(Estadocontrato, models.DO_NOTHING,
                                       db_column='EstadoFaturaID')  # Field name made lowercase.

    class Meta:
        db_table = 'Factura/Recibo'
