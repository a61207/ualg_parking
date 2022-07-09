from django.contrib import messages
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from main.models import *
from reserves.forms import ReclamacaoForm, ComprovativoForm, ContratoForm


def criar_reserva(request, id):
    estados = Estadoreserva.objects.all()
    parque = ParkingSpot.objects.get(id=id).zone.park.name
    client = Client.objects.get(user=request.user)
    if estados:
        if request.method == 'POST':
            print(request.POST)
            dataI = request.POST['datastart']
            dataF = request.POST['dataend']
            matricula = request.POST['matricula']
            viatura = Car.objects.get(registration=matricula)
            period = Periocidade.objects.create(start=dataI, end=dataF)
            lugar = ParkingSpot.objects.get(id=id)
            Reserva.objects.create(userid=client, lugarid=lugar, parqueid=lugar.zone.park,
                                   periocidadeid=period, matricula=viatura)
            messages.add_message(request, messages.SUCCESS, "Reserva in park '" + parque + "' created")
            return HttpResponseRedirect(reverse('listarReservas'))
        else:
            return render(request, 'criarReserva.html',
                          {'estados': estados, 'id': id})
    return HttpResponseNotFound()


def listar_reservas(request):
    reservas = Reserva.objects.all().order_by('-editadoem')
    return render(request, 'listarReservas.html', {'reservas': reservas})


def visualizar_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    return render(request, 'reservas/visualizarReservas.html', {'reserva': reserva})


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
                estado = form.cleaned_data['estadoreservaid']
                dataI = request.POST['datainicio']
                dataF = request.POST['datafim']
                matricula = request.POST['matricula']
                viatura = Car.objects.get(registration=matricula)
                Contrato.objects.create(userid=client, lugarid=lugar, estadoreservaid=estado, datainicio=dataI,
                                        datafim=dataF, matricula=viatura)
                messages.add_message(request, messages.SUCCESS, "Contrato in park '" + parque.name + "' created")
                return HttpResponseRedirect(reverse('listarContratos'))
            else:
                parque_old = request.POST['parqueid']
                lugar_old = request.POST['lugarid']
                estado_old = request.POST['estadoreservaid']
                print(form.errors)
                return render(request, 'criarContrato.html',
                              {'estados': estados, 'erros': form.non_field_errors().as_text,
                               'estado_old': int(estado_old), 'parque_old': int(parque_old),
                               'lugar_old': int(lugar_old),
                               'parques': parques})
        else:
            return render(request, 'criarContrato.html',
                          {'estados': estados, 'parques': parques})
    return HttpResponseNotFound()


def listar_contratos(request):
    contratos = Contrato.objects.all().order_by('-editadoem')
    return render(request, 'listarContratos.html', {'contratos': contratos})


def visualizar_contrato(request, id):
    contrato = Contrato.objects.get(id=id)
    return render(request, 'visualizarContratos.html', {'contrato': contrato})


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

    return render(request, '../templates/paymentAndContractsManagement/FazerReclamação.html',
                  {'form': form, 'submit': submit})


def modalidade_pagamento(request, id):
    contratos = Contrato.objects.filter(userid=User.objects.get(id=id))
    return render(request, '../templates/paymentAndContractsManagement/ModalidadePagamento.html',
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
    return render(request, '../templates/paymentAndContractsManagement/ComprovarPagamento.html',
                  {'form': form, 'submit': submit})


def emitir_recibo(request, contrato_id):
    faturas = FacturaRecibo.objects.get(contratoid=contrato_id)
    return render(request, '../templates/paymentAndContractsManagement/Recibo.html',
                  {'faturas': faturas})


def listar_fatura(request, contrato_id):
    faturas = FacturaRecibo.objects.filter(contratoid=contrato_id)
    return render(request, '../templates/paymentAndContractsManagement/Fatura.html',
                  {'faturas': faturas})


def consultar_fatura(request, id):
    inicio = Periocidade.objects.filter(id=id)
    reclamacao = FacturaRecibo.objects.get(id=id)
    estado = FacturaRecibo.objects.filter(id=id, estadofaturaid=4)
    faturas = FacturaRecibo.objects.get(id=id)
    return render(request, '../templates/paymentAndContractsManagement/FaturaEspecifica.html',
                  {'faturas': faturas, 'reclamacao': reclamacao, 'estado': estado, 'inicio': inicio})


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