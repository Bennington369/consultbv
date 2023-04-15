from django import template
from django.contrib.auth.models import User

register = template.Library()

# registrar un filtro para agregar clases
# a elementos de formulario ya creado ( campos )
@register.filter(name='addclass')
def addclass(value, arg):
	return value.as_widget(attrs={'class':arg})

@register.filter(name='placeholder')
def placeholder(value, arg):
	return value.as_widget(attrs={'placeholder':arg})