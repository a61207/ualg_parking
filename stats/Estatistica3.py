import calendar
from datetime import *
from .forms import *
from main.models import *

def intervalo_horas_3(hora_inicio, hora_final, periocidades, data_inicio):
    data = []
    data2 = []
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    label = []

    hinicio = hora_inicio.split(":")

    hfinal = hora_final.split(":")
    sum = 0
    for h in range(int(hinicio[0]), int(hfinal[0])+1):
        sum = 0
        sum2 = 0
        perio = periocidades.filter(start__hour=h, start__year=dateStart.year, start__month = dateStart.month, start__day = dateStart.day)
        perioc = []
        for p in perio:
            perioc.append(p.id)
        reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
        reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
        data.append(reserva)
        data2.append(reserva2)
        label.append(str(h) + ":00")

    
    return data, label, data2

def intervalo_dias_3(data_inicio, data_final, periocidades):
    data = []
    data2 = []
    label = []
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()
    

    if (dateStart.month == dateEnd.month):
        for d in range(dateStart.day, dateEnd.day+1):
            sum = 0
            sum2 = 0
            perio = periocidades.filter(start__day=d)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
            data.append(reserva)
            data2.append(reserva2)
            label.append(d)
        return data, label, data2
    edge = calendar.monthrange(dateStart.year, dateStart.month)
    for d in range(dateStart.day, edge[1]+1):
            sum = 0
            sum2 = 0
            perio = periocidades.filter(start__month = dateStart.month, start__day=d)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
            data.append(reserva)
            data2.append(reserva2)
            label.append(d)
    if dateStart.month + 1 != dateEnd.month:
        edge = calendar.monthrange(dateStart.year, dateStart.month+1)
        for d in range(1, edge[1]+1):
            sum = 0
            sum2 = 0
            perio = periocidades.filter(start__month = dateStart.month+1, start__day=d)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
            data.append(reserva)
            data2.append(reserva2)
            label.append(d)
    for d in range(1, dateEnd.day+1):
        sum = 0
        sum2 = 0
        perio = periocidades.filter(start__month = dateEnd.month, start__day=d)
        perioc = []
        for p in perio:
            perioc.append(p.id)
        reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
        reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
        data.append(reserva)
        data2.append(reserva2)
        label.append(d)
    return data, label, data2

def intervalo_meses_3(data_inicio, data_final, periocidades):
    data=[]
    data2 = []
    label=[]
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()

    if (dateStart.year == dateEnd.year):
        for m in range(dateStart.month, dateEnd.month+1):
            sum = 0
            sum2 = 0
            perio = periocidades.filter(start__month = m)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
            data.append(reserva)
            data2.append(reserva2)
            label.append(m)
    else:
        for m in range(dateStart.month, 12+1):
            sum = 0
            sum2 = 0
            perio = periocidades.filter(start__month = m)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
            data.append(reserva)
            data2.append(reserva2)
            label.append(m)
        for m in range(1, dateEnd.month+1):
            sum = 0
            sum2 = 0
            perio = periocidades.filter(start__month = m)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
            data.append(reserva)
            data2.append(reserva2)
            label.append(m)
    return data, label, data2

def intervalo_anos_3(data_inicio, data_final, periocidades):
    data=[]
    data2=[]
    label=[]
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()

    for y in range(dateStart.year, dateEnd.year+1):
        sum = 0
        sum2 = 0
        perio = periocidades.filter(start__year = y)
        perioc = []
        for p in perio:
            perioc.append(p.id)
        reserva = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = True).count() 
        reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  contratoid__isnull = False).count()
        data.append(reserva)
        data2.append(reserva2)
        label.append(y)
    return data, label, data2


def intervaloTempo_3(data_inicio, hora_inicio, data_final, hora_final, periocidades):
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()
    d = dateEnd - dateStart
    if (d.days < 1): #ver em intervalo de horas
        return intervalo_horas_3(hora_inicio, hora_final, periocidades, data_inicio)
    elif (d.days <= 31): #ver em intervalo de dias
        return intervalo_dias_3(data_inicio, data_final, periocidades)
    elif (d.days<=365): #ver em intervalo de meses
        return intervalo_meses_3(data_inicio, data_final, periocidades)
    else: #ver em anos
        return intervalo_anos_3(data_inicio, data_final, periocidades)
