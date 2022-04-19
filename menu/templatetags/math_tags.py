from django import template

register = template.Library()


@register.filter(name='mult')
def mult(value, arg):
    return float(value) * float(arg)


@register.filter(name='mult_with_round')
def mult_with_round(value, arg):
    result = float(value) * float(arg)
    return round(result, 1)
