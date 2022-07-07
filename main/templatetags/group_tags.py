from django import template
from django.utils import timezone

from main.models import Administrator, Employee, Client

register = template.Library()


@register.filter(name='is_admin')
def is_admin(user):
    return Administrator.objects.filter(user=user.id).exists()


@register.filter(name='is_employee')
def is_employee(user):
    return Employee.objects.filter(user=user.id).exists()


@register.filter(name='is_client')
def is_client(user):
    return Client.objects.filter(user=user.id).exists()


@register.filter(name='is_staff')
def is_staff(user):
    return Employee.objects.filter(user=user.id).exists() or Administrator.objects.filter(user=user.id).exists()


@register.filter(name='get_park_occupied')
def get_park_occupied(park, deadline):
    return park.occupied_spots(deadline.start_date, deadline.end_date)


@register.filter(name='get_park_reserved')
def get_park_reserved(park, deadline):
    return park.reserved_spots(deadline.start_date, deadline.end_date)


@register.filter(name='get_park_not_free')
def get_park_not_free(park, deadline):
    return park.reserved_spots(deadline.start_date, deadline.end_date) + \
           park.occupied_spots(deadline.start_date, deadline.end_date)


@register.filter(name='get_park_all_not_free')
def get_park_all_not_free(park):
    return park.reserved_spots(timezone.now().date(), timezone.datetime.max) + \
           park.occupied_spots(timezone.now().date(), timezone.datetime.max)


@register.filter(name='get_zone_all_not_free')
def get_zone_all_not_free(zone):
    return zone.reserved_spots(timezone.now().date(), timezone.datetime.max) + \
           zone.occupied_spots(timezone.now().date(), timezone.datetime.max)


@register.filter(name='get_park_free')
def get_park_free(park, deadline):
    return park.free_spots(deadline.start_date, deadline.end_date)


@register.filter(name='get_non_achived_resources')
def get_non_achived_resources(park):
    return park.non_achived_resources()
