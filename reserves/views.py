from django.http import HttpResponseNotFound
from django.shortcuts import render

# Create your views here.
from parks.models import Park
from reserves.forms import ReservaForm
from reserves.models import Estadoreserva, Reserva, Contrato, FacturaRecibo


def criar_reserva(request):
    estados = Estadoreserva.objects.all()
    parques = Park.objects.all().order_by('-updated')
    if parques and estados:
        if request.method == 'POST':
            form = ReservaForm(request.POST)
            if form.is_valid():
                parque = form.cleaned_data['parqueid']
                lugar = form.cleaned_data['lugarid']
                estado = form.cleaned_data['estadoreservaid']
                Reserva.objects.create(userid=request.user, parqueid=parque, lugarid=lugar, estadoreservaid=estado)
                return render(request, 'index.html')
            # TODO por mensagens de sucesso
            else:
                parque_old = request.POST['parqueid']
                lugar_old = request.POST['lugarid']
                estado_old = request.POST['estadoreservaid']
                print(form.errors)
                return render(request, 'reservas/criarReserva.html',
                              {'estados': estados, 'erros': form.non_field_errors().as_text,
                               'estado_old': int(estado_old), 'parque_old': int(parque_old),
                               'lugar_old': int(lugar_old),
                               'parques': parques})
        else:
            return render(request, 'reservas/criarReserva.html',
                          {'estados': estados, 'parques': parques})
    return HttpResponseNotFound()


def listar_reservas(request):
    reservas = Reserva.objects.all().order_by('-editadoem')
    return render(request, 'reservas/listarReservas.html', {'reservas': reservas})


def visualizar_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    return render(request, 'reservas/visualizarReservas.html', {'reserva': reserva})


def apagar_reserva(request, id):
    reserva = Reserva.objects.get(id=id)
    if request.method == 'POST':
        reserva.delete()
        return render(request, 'index.html')
        # TODO por mensagens de sucesso
    else:
        return render(request, 'reservas/apagarReserva.html', {'reserva': reserva})


def criar_contrato(request):
    pass


def listar_contratos(request):
    contratos = Contrato.objects.all().order_by('-editadoem')
    return render(request, 'contratos/listarContratos.html', {'contratos': contratos})


def visualizar_contrato(request):
    pass


def cancelar_contrato(request):
    pass


def listar_fatura(request, contrato_id):
    faturas = FacturaRecibo.objects.filter(contratoid=contrato_id)
    return render(request, 'paymentAndContractsManagement/Fatura.html',
                  {'faturas': faturas})


def consultar_fatura(request, id):
    faturas = FacturaRecibo.objects.get(id=id)
    print(faturas)
    return render(request, 'paymentAndContractsManagement/FaturaEspecifica.html',
                  {'fatura': faturas})


def comprovativo_pagamento(request, id):
    contratos = Contrato.objects.get(id=id)
    return render(request, 'paymentAndContractsManagement/ComprovarPagamento.html',
                  {'contratos': contratos})