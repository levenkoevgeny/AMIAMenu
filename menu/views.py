import datetime
from datetime import datetime

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import F

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import MenuDay, Product, ProductGroup, MealTime, Map, MapsInMenuDay, ProductsInMap, DishCategory, \
    TreatmentKind, WastageByDateRange
from .serializers import ProductSerializer, ProductGroupSerializer, MapSerializer, ProductsInMapSerializer, \
    MapsInMenuDaySerializer, MealTimeSerializer, MenuDaySerializer, WastageByDateRangeSerializer
from .filters import MenuDayFilter, ProductGroupFilter, ProductFilter, MapFilter

from dateutil.relativedelta import *


def menu_items(request):

    if 'menu_day_date_start' in request.GET and 'menu_day_date_end' in request.GET:
        f = MenuDayFilter(request.GET, queryset=MenuDay.objects.all())
        menu_days = f.qs
    else:
        f = MenuDayFilter(request.GET, queryset=MenuDay.objects.filter(menu_day_date=datetime.now().date()))
        menu_days = f.qs

    products_group = ProductGroup.objects.all()
    products_group_main = products_group.filter(replacement_for=F('pk'))

    if 'menu_day_date_start' in request.GET and 'menu_day_date_end' in request.GET:

        date_start_str = request.GET['menu_day_date_start'] if request.GET['menu_day_date_start'] != '' else str(datetime.now().date())
        date_end_str = request.GET['menu_day_date_end'] if request.GET['menu_day_date_end'] != '' else str(datetime.now().date())

        date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()
    else:
        date_start = datetime.now().date()
        date_end = datetime.now().date()

    return render(request, 'menu/menu-items.html', {
        'today': datetime.now().date(),
        'date_start': date_start,
        'date_end': date_end,
        'day_count': relativedelta(date_end, date_start).days + 1,
        'dates_str': str(date_start) + ',' + str(date_end),
        'menu_days': menu_days,
        'filter': f,
        'products_group': products_group,
        'products_group_main': products_group_main,
        'products_all': Product.objects.all(),
        'meal_times': MealTime.objects.all(),
        'maps': Map.objects.all(),
        'maps_id_list': [map.map.id for map in MapsInMenuDay.objects.filter(menu_day__in=menu_days)],
        'dish_categories': DishCategory.objects.all()
    })


def product_groups(request):
    product_group_list = ProductGroup.objects.all()
    f = ProductGroupFilter(request.GET, queryset=product_group_list.filter(replacement_for=F('pk')))
    products_group_list_main = f.qs

    return render(request, 'menu/product/product_group_list.html', {
        'product_group_list': product_group_list,
        'products_group_list_main': products_group_list_main,
        'products_group_list_not_main': product_group_list.exclude(replacement_for=F('pk')),
        'filter': f,
    })


def products(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    products_list = f.qs
    treatment_kind_list = TreatmentKind.objects.all().order_by('id')
    wastage_list = WastageByDateRange.objects.all()
    return render(request, 'menu/product/products_list.html', {
        'products_list': products_list,
        'filter': f,
        'treatment_kind_list': treatment_kind_list,
        'wastage_list': wastage_list
    })


def maps(request):
    f = MapFilter(request.GET, queryset=Map.objects.all())
    maps_list = f.qs
    return render(request, 'menu/map/maps_list.html', {
        'maps_list': maps_list,
        'filter': f,
    })


def maps_items(request, map_id):
    if 'menu_date' in request.GET:
        menu_date = datetime.strptime(request.GET['menu_date'], '%Y-%m-%d').date()
    else:
        menu_date = datetime.now().date()
    product_list = Product.objects.all()
    map_with_items = get_object_or_404(Map, pk=map_id)
    return render(request, 'menu/map/maps_items.html', {
        'product_list': product_list,
        'map_with_items': map_with_items,
        'dish_categories': DishCategory.objects.all(),
        'product_group_list': ProductGroup.objects.all(),
        'treatments': TreatmentKind.objects.all().order_by('id'),
        'net_weights': map_with_items.get_net_weights_by_dish_category(menu_date),
        'values': map_with_items.get_values(menu_date),
        'menu_date': menu_date,
    })


# Viewsets for REST API

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductGroupViewSet(viewsets.ModelViewSet):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer


class ProductsInMapViewSet(viewsets.ModelViewSet):
    queryset = ProductsInMap.objects.all()
    serializer_class = ProductsInMapSerializer


class MapsInMenuDayViewSet(viewsets.ModelViewSet):
    queryset = MapsInMenuDay.objects.all()
    serializer_class = MapsInMenuDaySerializer


class MealTimeViewSet(viewsets.ModelViewSet):
    queryset = MealTime.objects.all()
    serializer_class = MealTimeSerializer


class MenuDayViewSet(viewsets.ModelViewSet):
    queryset = MenuDay.objects.all()
    serializer_class = MenuDaySerializer


class WastageByDateRangeViewSet(viewsets.ModelViewSet):
    queryset = WastageByDateRange.objects.all()
    serializer_class = WastageByDateRangeSerializer


@api_view(['POST'])
def menu_day_update_maps(request):
    menu_day = get_object_or_404(MenuDay, pk=request.data['menu_day_id'])
    menu_day.mapsinmenuday_set.all().delete()

    for meal in MealTime.objects.all():
        meal_time = get_object_or_404(MealTime, pk=meal.id)
        request_maps_list = request.data[str(meal.id)]
        for map_id in request_maps_list:
            map_ = get_object_or_404(Map, pk=map_id)
            MapsInMenuDay.objects.create(menu_day=menu_day, map=map_, meal_time=meal_time)
    return Response('Ok', status.HTTP_200_OK)