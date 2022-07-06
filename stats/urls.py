from django.urls import path

from stats import views

urlpatterns = [
    path("estatistica/", views.menuEstatisticas, name="menuEstatisticas"),
    # path("estatistica/finalDay", views.finalDay, name="finalDay"),
    # path("estatistica/finalMonth", views.finalMonth, name="finalMonth"),
    # path("estatistica/finalYear", views.finalYear, name="finalYear"),
    path("estatistica/menu", views.menu, name="menu"),
    path("estatistica/Grafico1", views.Grafico1, name="Grafico1"),
    path("estatistica/Grafico2", views.Grafico2, name="Grafico2"),
    path("estatistica/Grafico3", views.Grafico3, name="Grafico3"),
    path("estatistica/Grafico4", views.Grafico4, name="Grafico4"),

    # --------------------------individual (cliente)------------------------

    path("estatistica/Grafico5", views.Grafico5, name="Grafico5"),
    path("estatistica/Grafico6", views.Grafico6, name="Grafico6"),
    path("estatistica/Grafico7", views.Grafico7, name="Grafico7"),
]
