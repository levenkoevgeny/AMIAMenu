from django import template

register = template.Library()


@register.filter(name='get_sub_dict')
def get_sub_dict(value, index):
    return round(value[index], 2)
