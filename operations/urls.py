from django.urls import path
from . import views

urlpatterns = [
    # Gestão de Operações
    path('portaria', views.portaria, name='portaria'),
    path('portaria/entrar', views.entrar_parque, name='entrarParque'),
    path('portaria/sair', views.sair_parque, name='sairParque'),
    path('registarEntradaReserva/<int:id>/<int:entrada>', views.registar_entrada_res,
         name='registarEntradaReserva'),
    path('registarEntradaContrato/<int:id>/<int:entrada>', views.registar_entrada_con,
         name='registarEntradaContrato'),
    path('registarSaidaReserva/<int:id>/<int:saida>', views.registar_saida_res,
         name='registarSaidaReserva'),
    path('registarSaidaContrato/<int:id>/<int:saida>', views.registar_saida_con,
         name='registarSaidaContrato'),
    path('ocuparLugar/<int:id>', views.ocupar_lugar, name='ocuparLugar'),
    path('libertarLugar/<int:id>/<int:lugarid>', views.libertar_lugar, name='libertarLugar'),
    path('associar/<int:id>', views.associar_lugar, name='associarLugar'),
    path('desassociar/<int:id>', views.desassociar_lugar, name='desassociarLugar'),
    path('entradassaidas', views.entradassaidas, name='entradassaidas'),
    path('pagamento/<int:id>', views.pagamento, name='pagamento'),
    path('recibo/<int:id>', views.recibo, name='recibo'),
    path('parking_spots/', views.listar_lugares, name='listarLugares'),
    path('parks/<park>/zones/<zone>/spot/<int:id>', views.visualizar_lugar, name='visualizarLugar'),
]
