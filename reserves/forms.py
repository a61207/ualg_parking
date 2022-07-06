# Formulario para criar reservas
from django import forms

from main.models import *


class ReservaForm(forms.ModelForm):
    estadoreservaid = forms.ModelChoiceField(queryset=Estadoreserva.objects.all(),
                                             error_messages={'required': 'Name of the address must be defined.',
                                                             'unique': 'Name of the address already exists'})

    class Meta:
        model = Reserva
        fields = ("estadoreservaid",)


# Formulario da Reclamação
class ReclamacaoForm(forms.ModelForm):
    class Meta:
        model = Reclamacao
        fields = ('nome', 'email', 'telefone', 'descricao')


# Formulario do Comprovativo
class ComprovativoForm(forms.ModelForm):
    class Meta:
        model = FacturaRecibo
        fields = ('comprovativopagamento',)


# Formulario para criar contratos
class ContratoForm(forms.ModelForm):
    parqueid = forms.ModelChoiceField(queryset=Park.objects.all(),
                                      error_messages={'required': 'Name of parque must be defined.',
                                                      'unique': 'Name of parque already exists'})
    zonaid = forms.ModelChoiceField(queryset=Zone.objects.all(),
                                    error_messages={'required': 'Name of lugar must be defined.',
                                                    'unique': 'Name of lugar already exists'})
    lugarid = forms.ModelChoiceField(queryset=ParkingSpot.objects.all(),
                                     error_messages={'required': 'Name of lugar must be defined.',
                                                     'unique': 'Name of lugar already exists'})
    estadoreservaid = forms.ModelChoiceField(queryset=Estadoreserva.objects.all(),
                                             error_messages={'required': 'Name of the address must be defined.',
                                                             'unique': 'Name of the address already exists'})

    class Meta:
        model = Contrato
        fields = ("parqueid", "zonaid", "lugarid", "estadoreservaid")
