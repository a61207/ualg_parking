from django import forms
from django.core.exceptions import NON_FIELD_ERRORS

from main.models import *


# Formulario para entrar no parque
class EntrarForm(forms.ModelForm):
    class Meta:
        model = EntradasSaidas
        fields = ("periocidadeid", "matriculaviatura")


# Formulario para sair do parque
class SairForm(forms.ModelForm):
    class Meta:
        model = EntradasSaidas
        fields = ("periocidadeid", "matriculaviatura")
