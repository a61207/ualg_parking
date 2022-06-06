from django import template
from django.contrib.auth.models import Group

from main.models import Administrator

register = template.Library()


@register.filter(name='is_admin')
def is_admin(user):
    return Administrator.objects.filter(user=user.id).exists()
