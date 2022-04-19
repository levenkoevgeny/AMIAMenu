from django import template
from django.db.models import Sum

from menu.models import Map, ProductsInMap, Product, DishCategory

register = template.Library()


@register.filter(name='get_meal_items')
def get_meal_items(value, meal_time):
    maps_in_menu_day = value.filter(meal_time=meal_time)
    maps_list = [item.map.id for item in maps_in_menu_day]
    return Map.objects.filter(id__in=maps_list)


@register.filter(name='get_map_gross_by_product_group')
def get_map_gross_by_product_group(value, product_group):
    result = round(value.get_product_group_value(product_group), 2)
    return result if result > 0 else ''


@register.filter(name='get_map_gross_by_product_group_day')
def get_map_gross_by_product_group_day(menu_day, product_group):
    result = ProductsInMap.objects.filter(map__menuday=menu_day, group__replacement_for=product_group).aggregate(Sum('product_count_gross_normalize'))['product_count_gross_normalize__sum']
    if result:
        return round(result, 2) if result > 0 else ''
    else:
        return ''


@register.filter(name='get_map_gross_by_product_group_dates_interval')
def get_map_gross_by_product_group_dates_interval(menu_days, product_group):
    result = ProductsInMap.objects.filter(map__menuday__in=menu_days, group__replacement_for=product_group).aggregate(
        Sum('product_count_gross_normalize'))['product_count_gross_normalize__sum']
    if result:
        return round(result, 2) if result > 0 else ''
    else:
        return ''


# получить продукты использованные во всех картах
@register.filter(name='get_all_products_in_group_dates_interval')
def get_all_products_in_group_dates_interval(maps_id_list, product_group):
    products = Product.objects.filter(productsinmap__map__in=maps_id_list, productsinmap__group__replacement_for=product_group).distinct()
    return products


@register.filter(name='get_product_count_in_map')
def get_product_count_in_map(map, product):
    count = map.get_product_count(product)
    return count if count > 0 else ''


@register.filter(name='get_product_count_in_map_day')
def get_product_count_in_map_day(menu_day, product):
    result = ProductsInMap.objects.filter(map__menuday=menu_day, product=product).aggregate(Sum('product_count_gross'))['product_count_gross__sum']
    if result:
        return round(result, 2) if result > 0 else ''
    else:
        return ''


@register.filter(name='get_product_count_interval')
def get_product_count_interval(menu_days, product):
    result = ProductsInMap.objects.filter(map__menuday__in=menu_days, product=product).aggregate(Sum('product_count_gross'))['product_count_gross__sum']
    if result:
        return round(result, 2) if result > 0 else ''
    else:
        return ''


@register.filter(name='get_net_weights')
def get_net_weights(map, date):
    return map.get_net_weights_by_dish_category(date)


@register.filter(name='get_net_weights_day')
def get_net_weights_day(menu_day, date):
    net_weight_dict = {}
    for dish_category in DishCategory.objects.all():
        net_weight = 0
        for map in menu_day.technological_maps.all():
            net_weight += map.get_net_weights_by_dish_category(menu_day.menu_day_date)[dish_category.id]
        net_weight_dict[dish_category.id] = net_weight
    full_net_weight = 0
    for k in net_weight_dict:
        full_net_weight += net_weight_dict[k]
    net_weight_dict['full_net_weight'] = full_net_weight
    return net_weight_dict


@register.filter(name='get_net_weights_interval')
def get_net_weights_interval(menu_days, date):
    net_weight_dict = {}
    for dish_category in DishCategory.objects.all():
        net_weight = 0
        for menu_day in menu_days:
            for map in menu_day.technological_maps.all():
                net_weight += map.get_net_weights_by_dish_category(menu_day.menu_day_date)[dish_category.id]
        net_weight_dict[dish_category.id] = net_weight
    full_net_weight = 0
    for k in net_weight_dict:
        full_net_weight += net_weight_dict[k]
    net_weight_dict['full_net_weight'] = full_net_weight
    return net_weight_dict


# три метода для вычисления энергетической ценности (1 - для одной карты, 2 - для дня, 3 - для интервала).
# Можно было сделать однотипные методы для получения всех данных (белки, жиры, углеводы, энергетическая ценность)

@register.filter(name='get_values')
def get_values(map, date):
    return map.get_values(date)


@register.filter(name='get_energy_day')
def get_energy_day(menu_day, date):
    energy_sum = 0
    for map in menu_day.technological_maps.all():
        energy_sum += map.get_values(menu_day.menu_day_date)['energy']
    return round(energy_sum, 2) if energy_sum > 0 else ''


@register.filter(name='get_energy_interval')
def get_energy_interval(menu_days, date):
    energy_sum = 0
    for menu_day in menu_days:
        for map in menu_day.technological_maps.all():
            energy_sum += map.get_values(menu_day.menu_day_date)['energy']
    return round(energy_sum, 2) if energy_sum > 0 else ''
