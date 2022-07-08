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
from django.urls import path, include

import parks
from parks.views import ViewParkList
from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    # path('', views.Index.as_view(), name='index'),
    path('', parks.views.ViewParkList.as_view(), name='index'),
    path('signin/', views.SignIn.as_view(), name='signin'),
    path('account/<pk>/cars/', views.ViewCarsList.as_view(), name='cars'),
    path('account/<pk>/cars/add/', views.AddCar.as_view(), name='add_car'),
    path('account/<user>/cars/<pk>/update/', views.UpdateCar.as_view(), name='update_car'),
    path('account/<user>/cars/<pk>/delete/', views.DeleteCar.as_view(), name='delete_car'),
    path('employees/', views.ViewEmployeeList.as_view(), name='employees'),
    path('employees/<pk>/delete/', views.DeleteEmployee.as_view(), name='remove_employee'),
    path('administrators/<pk>/delete/', views.DeleteAdministrator.as_view(), name='remove_admin'),
    path('administrators/', views.ViewAdministratorsList.as_view(), name='administrators'),
    path('roles/', views.ViewRoleRequestList.as_view(), name='roles'),
]
