from django import template
register = template.Library()


@register.filter(name='get_wastage_by_treatment')
def get_wastage_by_treatment(value, treatment_kind):
    return value.filter(treatment_kind=treatment_kind)


@register.filter(name='get_sub_norm_from_main')
def get_sub_norm_from_main(value, main_norm):
    return value.filter(replacement_for__productgroup=main_norm)