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
    path('parks/add/', views.AddPark.as_view(), name='add_park'),
    path('parks/<pk>/price/add/', views.AddPriceType.as_view(), name='add_price'),
    path('parks/<pk>/contract/add/', views.AddContractType.as_view(), name='add_contract'),
    path('parks/', views.ViewParkList.as_view(), name='list_parks'),
    path('parks/<pk>/', views.ViewParkDetail.as_view(), name='park_detail'),
    path('parks/<pk>/update/', views.UpdatePark.as_view(), name='update_park'),
    path('parks/<pk>/price/update/', views.UpdatePriceType.as_view(), name='update_price'),
    path('parks/<pk>/contract/update/', views.UpdateContractType.as_view(), name='update_contract'),
    path('parks/<pk>/delete/', views.DeletePark.as_view(), name='delete_park'),
    path('parks/<park>/zones/add/', views.AddZone.as_view(), name='add_zone'),
    path('parks/<park>/zones/', views.ViewZoneList.as_view(), name='list_zones'),
    path('parks/<park>/zones/<pk>/', views.ViewZoneDetail.as_view(), name='zone_detail'),
    path('parks/<park>/zones/<pk>/update/', views.UpdateZone.as_view(), name='update_zone'),
    path('parks/<park>/zones/<pk>/delete/', views.DeleteZone.as_view(), name='delete_zone'),
]
