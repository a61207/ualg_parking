"""ualgParking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [

    # CRUD Reservas
    path('reserves/add/', views.criar_reserva, name='criarReserva'),
    path('reserves/', views.listar_reservas, name='listarReservas'),
    path('reserves/<int:id>', views.visualizar_reserva, name='visualizarReserva'),
    path('reserves/delete/<int:id>', views.apagar_reserva, name='apagarReserva'),

    # CRUD Contratos
    path('contracts/add/', views.criar_contrato, name='criarContrato'),
    path('contracts/', views.listar_contratos, name='listarContratos'),
    path('contracts/<int:id>', views.visualizar_contrato, name='visualizarContrato'),
    path('contracts/delete/<int:id>', views.cancelar_contrato, name='cancelarContrato'),

    path('fatura/<int:contrato_id>', views.listar_fatura, name='fatura'),
    path('consultar_fatura/<int:id>', views.consultar_fatura,
         name='consultar_fatura_especifica'),
    path('comprovativopagamento/<int:id>', views.comprovativo_pagamento,
         name='comprovativo_pagamento'),
]
