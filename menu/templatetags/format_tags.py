from django import template
from django.template.defaultfilters import floatformat
register = template.Library()


@register.filter(name='formatted_float')
def formatted_float(value):
    value = floatformat(value, arg=1)
    return str(value).replace(',', '.')