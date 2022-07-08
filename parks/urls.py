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
    path('test/', views.AddWeekDaySchedule.as_view(), name='test'),

    path('parks/add/', views.AddPark.as_view(), name='add_park'),
    path('parks/<pk>/price/add/', views.AddPriceTable.as_view(), name='add_price'),
    path('parks/<pk>/schedule/add/', views.AddWeekDaySchedule.as_view(), name='add_schedule'),
    path('parks/', views.ViewParkList.as_view(), name='list_parks'),
    path('parks/<pk>/', views.ViewParkDetail.as_view(), name='park_detail'),
    path('parks/<pk>/schedule/', views.ViewWeekDayScheduleList.as_view(), name='list_schedules'),
    path('parks/<pk>/price/', views.ViewPriceTableList.as_view(), name='list_prices'),
    path('parks/<pk>/update/', views.UpdatePark.as_view(), name='update_park'),
    path('parks/<park>/schedule/<pk>/update/', views.UpdateWeekDaySchedule.as_view(), name='update_schedule'),
    path('parks/<park>/price/<pk>/update/', views.UpdatePriceType.as_view(), name='update_price'),
    path('parks/<pk>/archive/', views.ArchivePark.as_view(), name='archive_park'),
    path('parks/<park>/schedule/<pk>/archive/', views.ArquiveSchedule.as_view(), name='arquive_schedule'),
    path('parks/<park>/price/<pk>/archive/', views.ArquivePriceTable.as_view(), name='arquive_price'),
    path('parks/<park>/zones/add/', views.AddZone.as_view(), name='add_zone'),
    path('parks/<park>/zones/', views.ViewZoneList.as_view(), name='list_zones'),
    path('parks/<park>/zones/<pk>/', views.ViewZoneDetail.as_view(), name='zone_detail'),
    path('parks/<park>/zones/<pk>/update/', views.UpdateZone.as_view(), name='update_zone'),
    path('parks/<park>/zones/<pk>/archive/', views.ArchiveZone.as_view(), name='archive_zone'),
    path('parks/<park>/zones/<zone>/spot/<pk>/archive/', views.ArchiveSpot.as_view(), name='archive_spot'),
]
