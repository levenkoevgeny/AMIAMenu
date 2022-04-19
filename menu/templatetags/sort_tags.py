from django import template
register = template.Library()


@register.filter(name='sort_by')
def sort_by(value, field_name):
    return value.order_by(field_name)