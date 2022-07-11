from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseRedirect, FileResponse
from django.shortcuts import render, redirect

import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
# Create your views here.
from django.urls import reverse

from main.models import *
from reserves.forms import ReclamacaoForm, ComprovativoForm, ContratoForm, ReservaForm


def criar_reserva(request, id):
    estados = Estadoreserva.objects.all()
    parque = ParkingSpot.objects.get(id=id).zone.park.name
    client = Client.objects.get(user=request.user)
    cars = Car.objects.filter(client=client)
    if estados:
        if request.method == 'POST':
            print(request.POST)
            dataI = request.POST['datastart']
            dataF = request.POST['dataend']
            matricula = request.POST['matricula']
            period = Periocidade.objects.create(start=dataI, end=dataF)
            lugar = ParkingSpot.objects.get(id=id)
            Reserva.objects.create(userid=client, lugarid=lugar, parqueid=lugar.zone.park,
                                   periocidadeid=period, matricula=matricula)
            messages.add_message(request, messages.SUCCESS, "Reserva in park '" + parque + "' created")
            return HttpResponseRedirect(reverse('listarReservas'))
        else:
            return render(request, 'criarReserva.html',
                          {'estados': estados, 'id': id})
    return HttpResponseNotFound()


def listar_reservas(request):
    reservas = Reserva.objects.filter(userid=Client.objects.get(user=request.user))
    return render(request, 'listarReservas.html', {'reservas': reservas})


def visualizar_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    return render(request, 'reservas/visualizarReservas.html', {'reserva': reserva})


def editar_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    estados = Estadoreserva.objects.all()
    parque = ParkingSpot.objects.get(id=id).zone.park.name
    client = Client.objects.get(user=request.user)
    cars = Car.objects.filter(client=client)
    start = reserva.periocidadeid.start.strftime("%Y-%m-%dT%H:%m").__str__()
    end = reserva.periocidadeid.end.strftime("%Y-%m-%dT%H:%m").__str__()
    if estados:
        if request.method == 'POST':
            dataI = request.POST['datastart']
            dataF = request.POST['dataend']
            matricula = request.POST['matricula']
            period = Periocidade.objects.create(start=dataI, end=dataF)
            lugar = ParkingSpot.objects.get(id=id)

            Reserva.objects.filter(id=id).update(userid=client, lugarid=lugar, parqueid=lugar.zone.park,
                                                 periocidadeid=period, matricula=matricula)
            messages.add_message(request, messages.SUCCESS, "Reserva in park '" + parque + "' updated")
            return HttpResponseRedirect(reverse('listarReservas'))
        return render(request, 'reservas/editarReserva.html',
                      {'estados': estados, 'id': id, 'reserva': reserva, 'start': start, 'end': end})
    return HttpResponseNotFound()


def apagar_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    if request.method == 'POST':
        reserva.delete()
        messages.add_message(request, messages.SUCCESS, "Reserve Deleted")
        return HttpResponseRedirect(reverse('listarReservas'))
    else:
        return render(request, 'reservas/apagarReserva.html', {'reserva': reserva})


def criar_contrato(request):
    estados = Estadoreserva.objects.all()
    parques = Park.objects.all().order_by('-updated')
    client = Client.objects.get(user=request.user)
    if parques and estados:
        if request.method == 'POST':
            form = ContratoForm(request.POST)
            if form.is_valid():
                parque = form.cleaned_data['parqueid']
                lugar = form.cleaned_data['lugarid']
                dataI = request.POST['datainicio']
                dataF = request.POST['datafim']
                period = Periocidade.objects.create(start=dataI, end=dataF)
                matricula = request.POST['matricula']
                viatura = Car.objects.get(registration=matricula)
                Contrato.objects.create(userid=client, lugarid=lugar, periocidadeid=period,
                                        matricula=viatura)
                messages.add_message(request, messages.SUCCESS, "Contrato in park '" + parque.name + "' created")
                return HttpResponseRedirect(reverse('listarContratos'))
            else:
                parque_old = request.POST['parqueid']
                lugar_old = request.POST['lugarid']
                print(form.errors)
                return render(request, 'criarContrato.html',
                              {'estados': estados, 'erros': form.non_field_errors().as_text,
                               'parque_old': int(parque_old),
                               'lugar_old': int(lugar_old),
                               'parques': parques})
        else:
            return render(request, 'criarContrato.html',
                          {'estados': estados, 'parques': parques})
    return HttpResponseNotFound()


def listar_contratos(request):
    contratos = Contrato.objects.filter(userid=Client.objects.get(user=request.user)).order_by('-editadoem')
    return render(request, 'listarContratos.html', {'contratos': contratos})


def visualizar_contrato(request, id):
    contrato = Contrato.objects.get(id=id)
    return render(request, 'visualizarContratos.html', {'contrato': contrato})


def editar_contrato(request, id):
    contrato = Contrato.objects.get(id=id)
    estados = Estadoreserva.objects.all()
    parques = ParkingSpot.objects.get(id=id).zone.park.name
    client = Client.objects.get(user=request.user)
    start = contrato.periocidadeid.start.strftime("%Y-%m-%dT%H:%m").__str__()
    end = contrato.periocidadeid.end.strftime("%Y-%m-%dT%H:%m").__str__()
    if estados:
        if request.method == 'POST':
            parque = request.POST['parqueid']
            lugar = form.cleaned_data['lugarid']
            estado = request.POST['estadoreservaid']
            dataI = request.POST['datainicio']
            dataF = request.POST['datafim']
            period = Periocidade.objects.create(start=dataI, end=dataF)
            matricula = request.POST['matricula']
            viatura = Car.objects.get(registration=matricula)
            Contrato.objects.filter(id=id).update(userid=request.user, parqueid=parque, lugarid=lugar,
                                                  estadoreservaid=estado, periocidadeid=period, matricula=viatura)
            messages.add_message(request, messages.SUCCESS, "Contrato in park '" + parque.name + "' updated")
            return HttpResponseRedirect(reverse('listarContratos'))
        return render(request, 'contratos/editarContrato.html',
                      {'estados': estados, 'parques': parques, 'id': id, 'contrato': contrato, 'start': start,
                       'end': end})
    return HttpResponseNotFound()


def estender_contrato(request, id):
    contrato = Contrato.objects.get(id=id)
    parques = ParkingSpot.objects.get(id=id).zone.park.name
    client = Client.objects.get(user=request.user)
    start = contrato.periocidadeid.start.strftime("%Y-%m-%d").__str__()
    end = contrato.periocidadeid.end.strftime("%Y-%m-%d").__str__()
    if parques:
        if request.method == 'POST':
            dataI = request.POST['datainicio']
            dataF = request.POST['datafim']
            period = Periocidade.objects.create(start=dataI, end=dataF)
            Contrato.objects.filter(id=id).update(userid=request.user, periocidadeid=period)
            messages.add_message(request, messages.SUCCESS, "Contrato in park extended")
            return HttpResponseRedirect(reverse('listarContratos'))
        return render(request, 'contratos/estenderContrato.html', {'id': id, 'start': start, 'end': end})
    return HttpResponseNotFound()


def listar_pagamentos_contratos(request):
    faturas = FacturaRecibo.objects.all()
    return render(request, 'paymentAndContractsManagement/listarPagamentosContratos.html',
                  {'faturas': faturas})


def fazer_reclamacao(request, id):
    form = ReclamacaoForm
    submit = False
    if request.method == "POST":
        form = ReclamacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('consultar_fatura_especifica', id)
        else:
            form = ReclamacaoForm
            if 'submit' in request.GET:
                submit = True

    return render(request, 'paymentAndContractsManagement/FazerReclamação.html',
                  {'form': form, 'submit': submit})


def modalidade_pagamento(request, id):
    contratos = Contrato.objects.filter(userid=Client.objects.get(id=id))
    return render(request, 'paymentAndContractsManagement/ModalidadePagamento.html',
                  {'contratos': contratos})


def comprovativo_pagamento(request, id):
    form = ComprovativoForm
    submit = False
    if request.method == "POST":
        form = ComprovativoForm(request.POST, request.FILES)
        if form.is_valid():
            fatura = FacturaRecibo.objects.filter(id=id).first()
            fatura.comprovativopagamento = request.FILES.get('comprovativopagamento')
            print(fatura.comprovativopagamento)
            estado = Estadocontrato.objects.get(id=9)  # Estado Ativo id=9
            fatura.estadofaturaid = estado
            fatura.save()
            # return HttpResponseRedirect('?True')
            return redirect('consultar_fatura_especifica', id)
        else:
            form = ComprovativoForm
            if 'submit' in request.GET:
                submit = True
    return render(request, 'paymentAndContractsManagement/ComprovarPagamento.html',
                  {'form': form, 'submit': submit})


def emitir_recibo(request, contrato_id):
    faturas = FacturaRecibo.objects.get(contratoid=contrato_id)
    return render(request, 'paymentAndContractsManagement/Recibo.html',
                  {'faturas': faturas})


def listar_fatura(request, contrato_id):
    faturas = FacturaRecibo.objects.filter(contratoid=contrato_id)
    return render(request, 'paymentAndContractsManagement/Fatura.html',
                  {'faturas': faturas})


def consultar_fatura(request, id):
    inicio = Periocidade.objects.filter(id=id)
    reclamacao = FacturaRecibo.objects.get(id=id)
    estado = FacturaRecibo.objects.filter(id=id, estadofaturaid=5)
    faturas = FacturaRecibo.objects.get(id=id)
    estadofaturaid = faturas.estadofaturaid.id
    return render(request, 'paymentAndContractsManagement/FaturaEspecifica.html',
                  {'faturas': faturas, 'reclamacao': reclamacao, 'estado': estado, 'inicio': inicio,
                   'estadofaturaid': estadofaturaid})


def cancelar_fatura(request, id):
    faturas = FacturaRecibo.objects.get(id=id)
    faturas.delete()
    return redirect('listarContratos')


def cancelar_contrato(request, id):
    contrato = Contrato.objects.get(id=id)
    if request.method == 'POST':
        contrato.delete()
        messages.add_message(request, messages.SUCCESS, "Contract Deleted")
        return HttpResponseRedirect(reverse('listarContratos'))
    else:
        return render(request, 'cancelarContrato.html', {'contrato': contrato})


def detalhes_fatura(request, id):
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Courier", 12)
    faturas = FacturaRecibo.objects.get(id=id)
    estado = faturas.estadofaturaid.nome
    inicio = faturas.periocidadeid.start
    fim = faturas.periocidadeid.end
    emissao = faturas.emitidaem
    strInicio = (str)(inicio)
    strFim = (str)(fim)
    strEmissao = (str)(emissao)
    metodopagamento = faturas.contratoid.modalidadepagamentoid.nome
    preco = 1.5
    inicio0 = (int)(inicio.timestamp())
    fim0 = (int)(fim.timestamp())
    durac = fim0 - inicio0
    montante = (float)(durac * preco) / 3600
    strMontante = (str)(montante)

    lines = []

    L1 = "Detalhes da fatura:"
    L2 = " "
    L3 = " "
    L4 = "------------------------------------------------"
    L5 = "ESTADO:............................."
    L6 = "------------------------------------------------"
    L7 = "INÍCIO:................................"
    L8 = "FIM:.................................."
    L9 = "EMISSÃO:................................."
    L10 = "------------------------------------------------"
    L11 = "MÉTODO DE PAGAMENTO:..............................."
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
    lines.append(L5 + estado)
    lines.append(L6)
    lines.append(L7 + strInicio)
    lines.append(L8 + strFim)
    lines.append(L9 + strEmissao)
    lines.append(L10)
    lines.append(L11 + metodopagamento)
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
    return FileResponse(buf, as_attachment=True, filename='fatura.pdf')
