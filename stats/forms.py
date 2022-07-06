from main.models import *

from django.forms import *

from django import forms

from datetime import datetime

TipoEstatistica = (
    ("1", "asd"),
)

Dia = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
    ("8", "8"),
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ("13", "13"),
    ("14", "14"),
    ("15", "15"),
    ("16", "16"),
    ("17", "17"),
    ("18", "18"),
    ("19", "19"),
    ("20", "20"),
    ("21", "21"),
    ("22", "22"),
    ("23", "23"),
    ("24", "24"),
    ("25", "25"),
    ("26", "26"),
    ("27", "27"),
    ("28", "28"),
    ("29", "29"),
    ("30", "30"),
    ("31", "31"),
)

Mes = (
    ("1", "Janeiro"),
    ("2", "Fevereiro"),
    ("3", "Março"),
    ("4", "Abril"),
    ("5", "Maio"),
    ("6", "Junho"),
    ("7", "Julho"),
    ("8", "Agosto"),
    ("9", "Setembro"),
    ("10", "Outubro"),
    ("11", "Novembro"),
    ("12", "Dezembro"),
)

Ano = (
    ("2022", "2022"),
    ("2023", "2023"),
    ("2024", "2024"),
)

TipoDeGrafico = (
    ("1", "Barras"),
    ("2", "Tarte"),
    ("3", "Linhas"),
)


def get_now():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


###################   REWORK #################################


class Grafico1Form(forms.ModelForm):
    start = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label="Data inicial")
    starth = forms.DateField(widget=NumberInput(attrs={'type': 'time'}), label="Hora inicial")
    end = forms.DateField(widget=NumberInput(attrs={'type': 'date'}), label="Data final")
    endh = forms.DateField(widget=NumberInput(attrs={'type': 'time'}), label="Hora final")
    tipografico = forms.ChoiceField(choices=TipoDeGrafico, label="Selecione o tipo de gráfico")

    class Meta:
        model = EntradasSaidas
        fields = [
            'start',
            'starth',
            'end',
            'endh',
            'tipografico',
        ]


################### END REWORK   #############################

class dayForm(forms.ModelForm):
    tipoestatistica = forms.ChoiceField(choices=TipoEstatistica, label="Selecione a estatística a apresentar")
    pickday = forms.ChoiceField(choices=Dia, label="Selecione o dia pretendido")
    pickmonth = forms.ChoiceField(choices=Mes, label="Selecione o mês pretendido")
    pickyear = forms.ChoiceField(choices=Ano, label="Selecione o ano pretendido")
    tipografico = forms.ChoiceField(choices=TipoDeGrafico, label="Selecione o tipo de gráfico")

    class Meta:
        model = EntradasSaidas
        fields = [
            'tipoestatistica',
            'pickday',
            'pickmonth',
            'pickyear',
            'tipografico',
        ]


class monthForm(forms.ModelForm):
    tipoestatistica = forms.ChoiceField(choices=TipoEstatistica, label="Selecione a estatística a apresentar")
    pickmonth = forms.ChoiceField(choices=Mes, label="Selecione o mês pretendido")
    pickyear = forms.ChoiceField(choices=Ano, label="Selecione o ano pretendido")
    tipografico = forms.ChoiceField(choices=TipoDeGrafico, label="Selecione o tipo de gráfico")

    class Meta:
        model = EntradasSaidas
        fields = [
            'tipoestatistica',
            'pickmonth',
            'pickyear',
            'tipografico',
        ]


class yearForm(forms.ModelForm):
    tipoestatistica = forms.ChoiceField(choices=TipoEstatistica, label="Selecione a estatística a apresentar")
    # pickday = forms.ChoiceField(choices=Dia, label="Selecione o dia pretendido")
    # pickmonth = forms.ChoiceField(choices=Mes, label="Selecione o mês pretendido")
    pickyear = forms.ChoiceField(choices=Ano, label="Selecione o ano pretendido")
    tipografico = forms.ChoiceField(choices=TipoDeGrafico, label="Selecione o tipo de gráfico")

    class Meta:
        model = EntradasSaidas
        fields = [
            'tipoestatistica',
            #       'pickday',
            #       'pickmonth',
            'pickyear',
            'tipografico',
        ]
