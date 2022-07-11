from django.contrib.auth.decorators import permission_required
from django.http import FileResponse
from django.shortcuts import render, redirect
from datetime import datetime

from .forms import EntrarForm, SairForm
from main.models import *

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Create your views here.
@permission_required('main.portaria')
def portaria(request):
    return render(request, 'portaria.html')


@permission_required('main.entradassaidas')
def entradassaidas(request):
    entradassaidas = EntradasSaidas.objects.all()
    context = {"entradassaidas": entradassaidas}
    return render(request, 'entradassaidas.html', context)


@permission_required('main.entrar_parque')
def entrar_parque(request):
    form = EntrarForm()
    context = {"form": form}
    if request.method == 'POST':
        matricula = request.POST['matricula']
        entrada = request.POST['entrada']
        carro = Car.objects.filter(registration=matricula)
        reservasArr = []
        contratosArr = []
        reservas = Reserva.objects.filter(matricula=request.POST['matricula'])
        contratos = Contrato.objects.filter(matricula=carro.first())
        new_entrada = datetime.strptime(entrada, "%Y-%m-%dT%H:%M")
        timeEntrada = int(new_entrada.timestamp()) + 3600
        reservasEncontradas = False
        contratosEncontrados = False
        for reserva in reservas:
            lugar = reserva.lugarid
            periocidade = reserva.periocidadeid
            start = periocidade.start
            timeStart = int(start.timestamp())
            if timeEntrada >= timeStart:
                end = periocidade.end
                timeEnd = int(end.timestamp())
                if timeEntrada <= timeEnd:
                    reservasEncontradas = True
                    reservasArr.append(reserva)
        for contrato in contratos:
            lugar = contrato.lugarid
            start = contrato.periocidadeid.start
            start2 = datetime.combine(start, datetime.min.time())
            timeStart = int(start2.timestamp())
            if timeEntrada >= timeStart:
                end = contrato.periocidadeid.end
                end2 = datetime.combine(end, datetime.min.time())
                timeEnd = int(end2.timestamp())
                if timeEntrada <= timeEnd:
                    contratosEncontrados = True
                    contratosArr.append(contrato)
        if reservasEncontradas or contratosEncontrados:
            context = {"form": form, "reservas": reservasArr, "contratos": contratosArr,
                        "entrada": timeEntrada}
        else:
            context = {"form": form, "check": True}
        render(request, "entrarParque.html", context)
    return render(request, "entrarParque.html", context)


@permission_required('main.sair_parque')
def sair_parque(request):
    form = SairForm()
    context = {"form": form}
    if request.method == 'POST':
        matricula = request.POST['matricula']
        saida = request.POST['saida']
        carro = Car.objects.filter(registration=matricula)
        reservasArr = []
        contratosArr = []
        reservas = Reserva.objects.filter(matricula=request.POST['matricula'])
        contratos = Contrato.objects.filter(matricula=carro.first())
        new_saida = datetime.strptime(saida, "%Y-%m-%dT%H:%M")
        timeSaida = int(new_saida.timestamp()) + 3600
        reservasEncontradas = False
        contratosEncontrados = False
        for reserva in reservas:
            periocidade = reserva.periocidadeid
            start = periocidade.start
            timeStart = int(start.timestamp())
            if timeSaida >= timeStart:
                end = periocidade.end
                timeEnd = int(end.timestamp())
                reservasEncontradas = True
                reservasArr.append(reserva)
        for contrato in contratos:
            start = contrato.periocidadeid.start
            start2 = datetime.combine(start, datetime.min.time())
            timeStart = int(start2.timestamp())
            if timeSaida >= timeStart:
                end = contrato.periocidadeid.end
                end2 = datetime.combine(end, datetime.min.time())
                timeEnd = int(end2.timestamp())
                contratosEncontrados = True
                contratosArr.append(contrato)
        new_saida2 = int(new_saida.timestamp())
        request.session['this_saida'] = new_saida2
        if reservasEncontradas or contratosEncontrados:
            context = {"form": form, "reservas": reservasArr, "contratos": contratosArr,
                        "saida": timeSaida, "saida2": new_saida}
        else:
            context = {"form": form, "check": True}
        render(request, "sairParque.html", context)
    return render(request, "sairParque.html", context)


@permission_required('main.registar_entrada_res')
def registar_entrada_res(request, id, entrada):
    new_entrada = datetime.fromtimestamp(entrada)
    new_entrada2 = int(new_entrada.timestamp())
    request.session['this_entrada'] = new_entrada2
    periodo = Periocidade(start=new_entrada)
    periodo.save()
    reserva = Reserva.objects.get(id=id)
    lugar = reserva.lugarid
    entsaid = EntradasSaidas(matriculaviatura=reserva.matricula, periocidadeid=periodo, lugarid=lugar)
    tipoRes = "Reserva"
    entsaid.tipo = tipoRes
    entsaid.save()
    reserva.entradassaidasid = entsaid
    reserva.save()
    return redirect(entradassaidas)


@permission_required('main.registar_entrada_con')
def registar_entrada_con(request, id, entrada):
    new_entrada = datetime.fromtimestamp(entrada)
    periodo = Periocidade(start=new_entrada)
    periodo.save()
    contrato = Contrato.objects.get(id=id)
    lugar = contrato.lugarid
    entsaid = EntradasSaidas(matriculaviatura=contrato.matricula, periocidadeid=periodo, lugarid=lugar)
    tipoCon = "Contrato"
    entsaid.tipo = tipoCon
    entsaid.save()
    contrato.entradassaidasid = entsaid
    contrato.save()
    return redirect(entradassaidas)


@permission_required('main.registar_saida_res')
def registar_saida_res(request, id, saida):
    new_saida = datetime.fromtimestamp(saida)
    reserva = Reserva.objects.get(id=id)
    entsaid = reserva.entradassaidasid
    periodo = entsaid.periocidadeid
    periodo.end = new_saida
    periodo.save()
    return redirect(entradassaidas)


@permission_required('main.registar_saida_con')
def registar_saida_con(request, id, saida):
    new_saida = datetime.fromtimestamp(saida)
    contrato = Contrato.objects.get(id=id)
    entsaid = contrato.entradassaidasid
    periodo = entsaid.periocidadeid
    periodo.end = new_saida
    periodo.save()
    return redirect(entradassaidas)


@permission_required('main.ocupar_lugar')
def ocupar_lugar(request, id):
    EntradasSaidas.objects.filter(id=id).update(in_spot=True)
    return redirect(entradassaidas)


@permission_required('main.libertar_lugar')
def libertar_lugar(request, id, lugarid):
    EntradasSaidas.objects.filter(id=id).update(in_spot=False)
    return redirect(entradassaidas)


@permission_required('main.associar_lugar')
def associar_lugar(request, id):
    lugar = ParkingSpot.objects.get(id=id)
    context = {"lugar": lugar}
    if request.method == 'POST':
        matricula = request.POST['matricula']
        entrada = request.POST['entrada']
        carro = Car.objects.filter(registration=matricula)
        if carro.exists():
            new_entrada = datetime.strptime(entrada, "%Y-%m-%dT%H:%M")
            final_entrada = Periocidade(start=new_entrada)
            final_entrada.save()
            new_visit = Visit(lugarid=lugar, matriculaviatura=carro.first(), periocidadeid=final_entrada)
            new_visit.save()
            entsaid1 = EntradasSaidas(matriculaviatura=carro.first(), periocidadeid=final_entrada, lugarid=lugar, in_spot=True)
            tipoMan = "Manual"
            entsaid1.tipo = tipoMan
            entsaid1.save()
            return redirect(visualizar_lugar, id=id)
    return render(request, "associar.html", context)


# Função para visualizar o lugar com o id especifico
@permission_required('main.view_lugar')
def visualizar_lugar(request, id):
    lugar = ParkingSpot.objects.get(id=id)
    reservas = Reserva.objects.filter(lugarid=lugar).order_by('-criadoem').first()
    visitas = Visit.objects.filter(lugarid=lugar)
    entsaid = EntradasSaidas.objects.filter(lugarid=lugar).order_by('-criadoem').first()
    context = {"lugar": lugar, "visitas": visitas, "entsaid": entsaid, "reservas": reservas}
    return render(request, 'visualizarLugar.html', context)


# Função para listar todos os lugares
@permission_required('main.view_lugar')
def listar_lugares(request):
    lugares = ParkingSpot.objects.all()
    return render(request, 'listarLugares.html', {'lugares': lugares})


@permission_required('main.desassociar_lugar')
def desassociar_lugar(request, id):
    lugar = ParkingSpot.objects.get(id=id)
    context = {"lugar": lugar}
    if request.method == 'POST':
        saida = request.POST['saida']
        visita = Visit.objects.filter(lugarid=lugar).order_by('-criadoem').first()
        periocidade = visita.periocidadeid
        new_saida = datetime.strptime(saida, "%Y-%m-%dT%H:%M")
        periocidade.end = new_saida
        periocidade.save()
        entradasaida = request.session.get('this_entradasaida')
        EntradasSaidas.objects.filter(id=entradasaida).update(in_spot=False)
        return redirect(visualizar_lugar, id=id)
    return render(request, "desassociar.html", context)


@permission_required('main.pagamento')
def pagamento(request, id):
    reserva = Reserva.objects.get(id=id)
    validadeReserva = reserva.periocidadeid.end
    new_entrada2 = request.session.get('this_entrada')
    new_saida2 = request.session.get('this_saida')
    new_entrada1 = datetime.fromtimestamp(new_entrada2)
    new_saida1 = datetime.fromtimestamp(new_saida2)
    preco = 1.5
    precoMulta = 2
    entrada = new_entrada2
    saida = new_saida2
    limite2 = (int)(validadeReserva.timestamp())
    limite = limite2
    durac = saida - entrada
    excesso = saida - limite
    precoSem = (float)(durac * preco) / 3600
    multa = (float)(excesso * precoMulta) / 3600
    if saida <= limite:
        precoFinal = precoSem
        multa = 0
    else:
        precoFinal = precoSem + multa
    request.session['this_precoFinal'] = precoFinal
    request.session['this_multa'] = multa
    context = {"pagamento": pagamento, "reserva": reserva, "entrada": new_entrada1, "saida": new_saida1,
               "fim": new_saida2, "preco": precoFinal, "multa": multa}
    render(request, "pagamento.html", context)
    return render(request, "pagamento.html", context)


@permission_required('main.emitirrecibo')
def emitirrecibo(request, id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Courier", 12)
    reserva = Reserva.objects.get(id=id)
    new_entrada2 = request.session.get('this_entrada')
    new_saida2 = request.session.get('this_saida')
    new_entrada1 = datetime.fromtimestamp(new_entrada2)
    new_saida1 = datetime.fromtimestamp(new_saida2)
    new_entrada = str(new_entrada1)
    new_saida = str(new_saida1)
    precoFinal = request.session.get('this_precoFinal')
    multa = request.session.get('this_multa')
    strMulta = (str)(multa)
    strMontante = (str)(precoFinal)
    lugaar = (str)(reserva.lugarid.number)

    lines = []

    L1 = "RECIBO DE ESTACIONAMENTO:"
    L2 = " "
    L3 = " "
    L4 = "------------------------------------------------"
    L5 = "Matrícula:............................."
    L6 = "------------------------------------------------"
    L7 = "PARQUE:................................"
    L8 = "ZONA:.................................."
    L9 = "LUGAR:................................."
    L10 = "------------------------------------------------"
    L11 = "ENTRADA:..............................."
    L12 = "SAÍDA:................................."
    L13 = "------------------------------------------------"
    L14 = "MULTA:................................."
    L15 = "MONTANTE:.............................."
    L16 = "------------------------------------------------"
    L17 = " "
    L18 = " "
    L19 = "AGRADECEMOS A SUA PREFERÊNCIA"
    L20 = "VOLTE SEMPRE"
    L21 = " "
    L22 = " "
    L23 = " "
    L24 = "@ 2022 LES"
    L25 = "Design by Group 2"
    L26 = "€"

    lines.append(L1)
    lines.append(L2)
    lines.append(L3)
    lines.append(L4)
    lines.append(L5 + reserva.matricula)
    lines.append(L6)
    lines.append(L7 + reserva.lugarid.zone.park.name)
    lines.append(L8 + reserva.lugarid.zone.name)
    lines.append(L9 + lugaar)
    lines.append(L10)
    lines.append(L11 + new_entrada)
    lines.append(L12 + new_saida)
    lines.append(L13)
    lines.append(L14 + strMulta + L26)
    lines.append(L15 + strMontante + L26)
    lines.append(L16)
    lines.append(L17)
    lines.append(L18)
    lines.append(L19)
    lines.append(L20)
    lines.append(L21)
    lines.append(L22)
    lines.append(L23)
    lines.append(L24)
    lines.append(L25)

    for line in lines:
        textob.textLine(line)
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='recibo.pdf')
