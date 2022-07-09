import calendar
import json
from django.shortcuts import render
from datetime import *
from .Estatistica import intervaloTempo
from .Estatistica2 import intervaloTempo_2
from .Estatistica3 import intervaloTempo_3
from .Estatistica4 import intervaloTempo_4
from .Estatistica5 import intervaloTempo_5
from .Estatistica6 import intervaloTempo_6
from .Estatistica7 import intervaloTempo_7
from .forms import *
from main.models import *


# Create your views here.

# --------------------RESTART---------------------------------------------

def menu(request):
    return render(request, 'estatistica/menu.html')


def Grafico1(request):
    mensagem = ""
    mensagem2 = ""
    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()
    print(parque.today_opening_time())
    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.today_opening_time()
    endh = parque.today_closing_time()
    parques = Park.objects.all()

    tipografico = 1
    min = str(parque.today_opening_time())
    max = str(parque.today_closing_time())

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico1.html', context)
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    min = data[0] + 1
    for i in range(0, len(data)):
        if data[i] < min:
            min = int(data[i])
            info = label[i]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        'info': info,
        "type": type,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'label': json.dumps(dados[1]),
    }
    return render(request, 'estatistica/Grafico1.html', context)


def Grafico2(request):
    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()

    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.abertura
    endh = parque.fecho
    parques = Park.objects.all()

    tipografico = 1
    min = str(parque.abertura)
    max = str(parque.fecho)

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)
        mensagem = ""
        mensagem2 = ""
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico2.html', context)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo_2(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    data2 = dados[2]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        "type": type,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'data2': data2,
        'label': json.dumps(label),
    }
    return render(request, 'estatistica/Grafico2.html', context)


def Grafico3(request):
    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()

    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.abertura
    endh = parque.fecho
    parques = Park.objects.all()

    tipografico = 2
    min = str(parque.abertura)
    max = str(parque.fecho)

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)
        mensagem = ""
        mensagem2 = ""
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico3.html', context)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo_3(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    data2 = dados[2]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        "type": type,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'data2': data2,
        'label': json.dumps(label),
    }
    return render(request, 'estatistica/Grafico3.html', context)


def Grafico4(request):
    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()

    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.abertura
    endh = parque.fecho
    parques = Park.objects.all()

    tipografico = 2
    min = str(parque.abertura)
    max = str(parque.fecho)

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)
        mensagem = ""
        mensagem2 = ""
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico4.html', context)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo_4(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    data2 = dados[2]
    data3 = dados[3]
    data4 = dados[4]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        "type": type,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'label': json.dumps(label),
    }
    return render(request, 'estatistica/Grafico4.html', context)


# -------------------Estatisticas Cliente--------------------------------

def Grafico5(request):
    utilizador_id = int(request.POST.get("utilizador_id", "0"))
    utilizador = User.objects.filter(id=utilizador_id).first()
    if utilizador is None:
        utilizador = User.objects.first

    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()

    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.abertura
    endh = parque.fecho
    parques = Park.objects.all()
    utilizadores = User.objects.all()

    tipografico = 1
    min = str(parque.abertura)
    max = str(parque.fecho)

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        utilizador = User.objects.filter(id=utilizador_id).first()
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)
        mensagem = ""
        mensagem2 = ""
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                "utilizadores": utilizadores,
                'utilizador_id': utilizador_id,
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico5.html', context)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque, userid=utilizador_id)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo_5(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    data2 = dados[2]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        "type": type,
        'utilizadores': utilizadores,
        'utilizador_id': utilizador_id,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'data2': data2,
        'label': json.dumps(label),
    }
    return render(request, 'estatistica/Grafico5.html', context)


def Grafico6(request):
    utilizador_id = int(request.POST.get("utilizador_id", "0"))
    utilizador = User.objects.filter(id=utilizador_id).first()
    if utilizador is None:
        utilizador = User.objects.first

    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()

    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.abertura
    endh = parque.fecho
    parques = Park.objects.all()
    utilizadores = User.objects.all()

    tipografico = 2
    min = str(parque.abertura)
    max = str(parque.fecho)

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        utilizador = User.objects.filter(id=utilizador_id).first()
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)
        mensagem = ""
        mensagem2 = ""
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                "utilizadores": utilizadores,
                'utilizador_id': utilizador_id,
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico6.html', context)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque, userid=utilizador_id)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo_6(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    data2 = dados[2]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        "type": type,
        'utilizadores': utilizadores,
        'utilizador_id': utilizador_id,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'data2': data2,
        'label': json.dumps(label),
    }
    return render(request, 'estatistica/Grafico6.html', context)


def Grafico7(request):
    utilizador_id = int(request.POST.get("utilizador_id", "0"))
    utilizador = User.objects.filter(id=utilizador_id).first()
    if utilizador is None:
        utilizador = User.objects.first
    parque_id = int(request.POST.get("parque_id", "0"))
    parque = Park.objects.filter(id=parque_id).first()
    if parque is None:
        parque = Park.objects.first()

    start = datetime.date(datetime.now())
    end = datetime.date(datetime.now())
    starth = parque.abertura
    endh = parque.fecho
    parques = Park.objects.all()
    utilizadores = User.objects.all()

    tipografico = 2
    min = str(parque.abertura)
    max = str(parque.fecho)

    if request.method == "POST":
        start = request.POST.get("start", start)
        end = request.POST.get("end", end)
        utilizador = User.objects.filter(id=utilizador_id).first()
        parque = Park.objects.filter(id=parque_id).first()
        starth = request.POST.get("starth", starth)
        endh = request.POST.get("endh", endh)
        mensagem = ""
        mensagem2 = ""
        erro = False
        if starth > endh:
            erro = True
            mensagem2 = "A hora de início tem que ser superior à hora final"
        if start > end:
            erro = True
            mensagem = "A data de início tem que ser superior à data final"
        if erro:
            info = []
            data = []
            label = []
            dados = []
            context = {
                "start": str(start),
                "end": str(end),
                "starth": str(starth),
                "endh": str(endh),
                'min': starth,
                'max': endh,
                'info': info,
                "type": "bar",
                "utilizadores": utilizadores,
                'utilizador_id': utilizador_id,
                'parques': parques,
                'parque_id': parque_id,
                'data': data,
                'mensagem': mensagem,
                'mensagem2': mensagem2,
                'label': json.dumps(dados),
            }
            return render(request, 'estatistica/Grafico7.html', context)

        if starth < str(parque.abertura):
            starth = str(parque.abertura)
        if endh > str(parque.fecho):
            endh = str(parque.fecho)

        min = str(parque.abertura)
        max = str(parque.fecho)

    if tipografico == 1:
        type = "bar"
    elif tipografico == 2:
        type = "pie"
    elif tipografico == 3:
        type = "line"

    periocidades = Periocidade.objects.all()

    periocidades.filter(start__gte=start)

    t = datetime.strptime(str(end), "%Y-%m-%d").date()
    End_max = t + timedelta(days=1)

    periocidades.filter(end__lte=End_max)
    starth = str(starth)
    horas = starth.split(":")
    periocidades = periocidades.filter(start__hour__gte=horas[0])
    endh = str(endh)
    horas = endh.split(":")
    periocidades = periocidades.filter(start__hour__lte=horas[0])

    periocidades_ids = []
    for periocidade in periocidades:
        periocidades_ids.append(periocidade.id)

    reservas = Reserva.objects.filter(periocidadeid__in=periocidades_ids, parqueid=parque, userid=utilizador_id)

    periocidades = []
    for reserva in reservas:
        periocidades.append(reserva.periocidadeid.id)

    periocidades = Periocidade.objects.filter(id__in=periocidades)
    dados = intervaloTempo_4(str(start), str(starth), str(end), str(endh), periocidades)

    data = dados[0]
    label = dados[1]
    data2 = dados[2]
    data3 = dados[3]
    data4 = dados[4]

    context = {
        "start": str(start),
        "end": str(end),
        "starth": str(starth),
        "endh": str(endh),
        'min': starth,
        'max': endh,
        "type": type,
        "utilizadores": utilizadores,
        'utilizador_id': utilizador_id,
        'parques': parques,
        'parque_id': parque_id,
        'data': data,
        'data2': data2,
        'data3': data3,
        'data4': data4,
        'label': json.dumps(label),
    }
    return render(request, 'estatistica/Grafico7.html', context)
