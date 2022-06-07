# Formulario para criar reservas
from django import forms

from parks.models import Park, ParkingSpot
from reserves.models import Estadoreserva, Reserva


class ReservaForm(forms.ModelForm):
    parqueid = forms.ModelChoiceField(queryset=Park.objects.all(),
                                      error_messages={'required': 'Name of lugar must be defined.',
                                                      'unique': 'Name of the address already exists'})
    lugarid = forms.ModelChoiceField(queryset=ParkingSpot.objects.all(),
                                     error_messages={'required': 'Name of lugar must be defined.',
                                                     'unique': 'Name of the addresss already exists'})

    estadoreservaid = forms.ModelChoiceField(queryset=Estadoreserva.objects.all(),
                                             error_messages={'required': 'Name of the address must be defined.',
                                                             'unique': 'Name of the address already exists'})

    class Meta:
        model = Reserva
        fields = ("parqueid", "lugarid", "estadoreservaid")
