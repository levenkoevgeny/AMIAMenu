from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='get_net_weight_treatment_array_property')
def get_net_weight_treatment_array_property(item, menu_date):
    return item.get_net_weight_treatment_array(menu_date)