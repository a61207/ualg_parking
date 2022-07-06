import calendar
from datetime import *
from .forms import *
from main.models import *


def intervalo_horas(hora_inicio, hora_final, periocidades):
    data = []
    label = []

    hinicio = hora_inicio.split(":")

    hfinal = hora_final.split(":")

    for h in range(int(hinicio[0]), int(hfinal[0])+1):
        perio = periocidades.filter(start__hour=h).count()
        data.append(perio)
        label.append(str(h) + ":00")

    return data, label

def intervalo_dias(data_inicio, data_final, periocidades):
    data = []
    label = []
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()
    

    if (dateStart.month == dateEnd.month):
        for d in range(dateStart.day, dateEnd.day+1):
            perio = periocidades.filter(start__day=d).count()
            data.append(perio)
            label.append(d)
        return data, label
    edge = calendar.monthrange(dateStart.year, dateStart.month)
    for d in range(dateStart.day, edge[1]+1):
            perio = periocidades.filter(start__month = dateStart.month, start__day=d).count()
            data.append(perio)
            label.append(d)
    if dateStart.month + 1 != dateEnd.month:
        edge = calendar.monthrange(dateStart.year, dateStart.month+1)
        for d in range(1, edge[1]+1):
            perio = periocidades.filter(start__month = dateStart.month+1, start__day=d).count()
            data.append(perio)
            label.append(d)
    for d in range(1, dateEnd.day+1):
        perio = periocidades.filter(start__month = dateEnd.month, start__day=d).count()
        data.append(perio)
        label.append(d)
    return data, label

def intervalo_meses(data_inicio, data_final, periocidades):
    data=[]
    label=[]
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()

    if (dateStart.year == dateEnd.year):
        for m in range(dateStart.month, dateEnd.month+1):
            perio = periocidades.filter(start__month = m).count()
            data.append(perio)
            label.append(m)
    else:
        for m in range(dateStart.month, 12+1):
            perio = periocidades.filter(start__month = m).count()
            data.append(perio)
            label.append(m)
        for m in range(1, dateEnd.month+1):
            perio = periocidades.filter(start__month = m).count()
            data.append(perio)
            label.append(m)
    return data, label

def intervalo_anos(data_inicio, data_final, periocidades):
    data=[]
    label=[]
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()

    for y in range(dateStart.year, dateEnd.year+1):
        perio = periocidades.filter(start__year = y).count()
        data.append(perio)
        label.append(y)
    return data, label


def intervaloTempo(data_inicio, hora_inicio, data_final, hora_final, periocidades):
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()
    d = dateEnd - dateStart
    if (d.days <= 2): #ver em intervalo de horas
        return intervalo_horas(hora_inicio, hora_final, periocidades)
    elif (d.days <= 31): #ver em intervalo de dias
        return intervalo_dias(data_inicio, data_final, periocidades)
    elif (d.days<=365): #ver em intervalo de meses
        return intervalo_meses(data_inicio, data_final, periocidades)
    else: #ver em anos
        return intervalo_anos(data_inicio, data_final, periocidades)