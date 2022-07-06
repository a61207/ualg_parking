import calendar
from datetime import *
from .forms import *
from main.models import *

def intervalo_horas_7(hora_inicio, hora_final, periocidades):
    data = []
    data2 = []
    data3 = []
    data4 = []
    label = []

    hinicio = hora_inicio.split(":")

    hfinal = hora_final.split(":")
    
    for h in range(int(hinicio[0]), int(hfinal[0])+1):
        
        perio = periocidades.filter(start__hour=h)

        perioc = []
        for p in perio:
            perioc.append(p.id)
        reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
        reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
        getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
        chegou_atrasado = 0
        saiu_atrasado = 0
        for g in getreserva:
            periocidade = g.periocidadeid
            entrada = g.entradassaidasid.periocidadeid
            if entrada.start > periocidade.start:
                chegou_atrasado +=1
            if entrada.end > periocidade.end:
                saiu_atrasado +=1



        data.append(reserva)
        data2.append(reserva2)
        data3.append(chegou_atrasado)
        data4.append(saiu_atrasado)
        label.append(str(h) + ":00")

    
    return data, label, data2, data3, data4

def intervalo_dias_7(data_inicio, data_final, periocidades):
    data = []
    data2 = []
    data3 = []
    data4 = []
    label = []
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()
    

    if (dateStart.month == dateEnd.month):
        for d in range(dateStart.day, dateEnd.day+1):
            perio = periocidades.filter(start__day=d)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
            getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
            chegou_atrasado = 0
            saiu_atrasado = 0
            for g in getreserva:
                periocidade = g.periocidadeid
                entrada = g.entradassaidasid.periocidadeid
                if entrada.start > periocidade.start:
                    chegou_atrasado +=1
                if entrada.end > periocidade.end:
                    saiu_atrasado +=1
            data.append(reserva)
            data2.append(reserva2)
            data3.append(chegou_atrasado)
            data4.append(saiu_atrasado)
            label.append(d)
        return data, label, data2, data3, data4
    edge = calendar.monthrange(dateStart.year, dateStart.month)
    for d in range(dateStart.day, edge[1]+1):
            perio = periocidades.filter(start__month = dateStart.month, start__day=d)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
            getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
            chegou_atrasado = 0
            saiu_atrasado = 0
            for g in getreserva:
                periocidade = g.periocidadeid
                entrada = g.entradassaidasid.periocidadeid
                if entrada.start > periocidade.start:
                    chegou_atrasado +=1
                if entrada.end > periocidade.end:
                    saiu_atrasado +=1
            data.append(reserva)
            data2.append(reserva2)
            data3.append(chegou_atrasado)
            data4.append(saiu_atrasado)
            label.append(d)
    if dateStart.month + 1 != dateEnd.month:
        edge = calendar.monthrange(dateStart.year, dateStart.month+1)
        for d in range(1, edge[1]+1):
            perio = periocidades.filter(start__month = dateStart.month+1, start__day=d)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
            getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
            chegou_atrasado = 0
            saiu_atrasado = 0
            for g in getreserva:
                periocidade = g.periocidadeid
                entrada = g.entradassaidasid.periocidadeid
                if entrada.start > periocidade.start:
                    chegou_atrasado +=1
                if entrada.end > periocidade.end:
                    saiu_atrasado +=1
            data.append(reserva)
            data2.append(reserva2)
            data3.append(chegou_atrasado)
            data4.append(saiu_atrasado)
            label.append(d)
    for d in range(1, dateEnd.day+1):
        perio = periocidades.filter(start__month = dateEnd.month, start__day=d)
        perioc = []
        for p in perio:
            perioc.append(p.id)
        reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
        reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
        getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
        chegou_atrasado = 0
        saiu_atrasado = 0
        for g in getreserva:
            periocidade = g.periocidadeid
            entrada = g.entradassaidasid.periocidadeid
            if entrada.start > periocidade.start:
                chegou_atrasado +=1
            if entrada.end > periocidade.end:
                saiu_atrasado +=1
        data.append(reserva)
        data2.append(reserva2)
        data3.append(chegou_atrasado)
        data4.append(saiu_atrasado)
        label.append(d)
    return data, label, data2, data3, data4

def intervalo_meses_7(data_inicio, data_final, periocidades):
    data=[]
    data2 = []
    data3= []
    data4=[]
    label=[]
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()

    if (dateStart.year == dateEnd.year):
        for m in range(dateStart.month, dateEnd.month+1):
            perio = periocidades.filter(start__month = m)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
            getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
            chegou_atrasado = 0
            saiu_atrasado = 0
            for g in getreserva:
                periocidade = g.periocidadeid
                entrada = g.entradassaidasid.periocidadeid
                if entrada.start > periocidade.start:
                    chegou_atrasado +=1
                if entrada.end > periocidade.end:
                    saiu_atrasado +=1
            data.append(reserva)
            data2.append(reserva2)
            data3.append(chegou_atrasado)
            data4.append(saiu_atrasado)
            label.append(m)
    else:
        for m in range(dateStart.month, 12+1):
            perio = periocidades.filter(start__month = m)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
            getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
            chegou_atrasado = 0
            saiu_atrasado = 0
            for g in getreserva:
                periocidade = g.periocidadeid
                entrada = g.entradassaidasid.periocidadeid
                if entrada.start > periocidade.start:
                    chegou_atrasado +=1
                if entrada.end > periocidade.end:
                    saiu_atrasado +=1
            data.append(reserva)
            data2.append(reserva2)
            data3.append(chegou_atrasado)
            data4.append(saiu_atrasado)
            label.append(m)
        for m in range(1, dateEnd.month+1):
            perio = periocidades.filter(start__month = m)
            perioc = []
            for p in perio:
                perioc.append(p.id)
            reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
            reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
            getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
            chegou_atrasado = 0
            saiu_atrasado = 0
            for g in getreserva:
                periocidade = g.periocidadeid
                entrada = g.entradassaidasid.periocidadeid
                if entrada.start > periocidade.start:
                    chegou_atrasado +=1
                if entrada.end > periocidade.end:
                    saiu_atrasado +=1
            data.append(reserva)
            data2.append(reserva2)
            data3.append(chegou_atrasado)
            data4.append(saiu_atrasado)
            label.append(m)
    return data, label, data2, data3, data4

def intervalo_anos_7(data_inicio, data_final, periocidades):
    data=[]
    data2=[]
    data3=[]
    data4=[]
    label=[]
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()

    for y in range(dateStart.year, dateEnd.year+1):
        perio = periocidades.filter(start__year = y)
        perioc = []
        for p in perio:
            perioc.append(p.id)
        reserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False).count()#compareceu
        reserva2 = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = True).count()#nao compareceu
        getreserva = Reserva.objects.filter(periocidadeid__in=perioc,  entradassaidasid__isnull = False)
        chegou_atrasado = 0
        saiu_atrasado = 0
        for g in getreserva:
            periocidade = g.periocidadeid
            entrada = g.entradassaidasid.periocidadeid
            if entrada.start > periocidade.start:
                chegou_atrasado +=1
            if entrada.end > periocidade.end:
                saiu_atrasado +=1
        data.append(reserva)
        data2.append(reserva2)
        data3.append(chegou_atrasado)
        data4.append(saiu_atrasado)
        label.append(y)
    return data, label, data2, data3, data4


def intervaloTempo_7(data_inicio, hora_inicio, data_final, hora_final, periocidades):
    dateStart = datetime.strptime(data_inicio,"%Y-%m-%d").date()
    dateEnd = datetime.strptime(data_final,"%Y-%m-%d").date()
    d = dateEnd - dateStart
    if (d.days <= 2): #ver em intervalo de horas
        return intervalo_horas_7(hora_inicio, hora_final, periocidades)
    elif (d.days <= 31): #ver em intervalo de dias
        return intervalo_dias_7(data_inicio, data_final, periocidades)
    elif (d.days<=365): #ver em intervalo de meses
        return intervalo_meses_7(data_inicio, data_final, periocidades)
    else: #ver em anos
        return intervalo_anos_7(data_inicio, data_final, periocidades)
