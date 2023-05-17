import datetime
from datetime import datetime

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.db.models import F
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import F

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .models import MenuDay, Product, ProductGroup, MealTime, Map, MapsInMenuDay, ProductsInMap, DishCategory, \
    TreatmentKind, WastageByDateRange, DateRange
from .serializers import ProductSerializer, ProductGroupSerializer, MapSerializer, ProductsInMapListSerializer, \
    MapsInMenuDaySerializer, MealTimeSerializer, MenuDaySerializer, WastageByDateRangeSerializer, UserSerializer, \
    TreatmentKindSerializer, DateRangeSerializer, ProductGroupSerializerForSelect2, MapSerializerForSelect2, DishCategorySerializer, MapListSerializer, \
    ProductsInMapSerializer, ProductSerializerForSelect2
from .filters import MenuDayFilter, ProductGroupFilter, ProductFilter, MapFilter

from dateutil.relativedelta import *
from jose import jwt


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

        date_start_str = request.GET['menu_day_date_start'] if request.GET['menu_day_date_start'] != '' else str(
            datetime.now().date())
        date_end_str = request.GET['menu_day_date_end'] if request.GET['menu_day_date_end'] != '' else str(
            datetime.now().date())

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
        'net_weights': map_with_items.get_net_weights_by_dish_category_(menu_date),
        'values': map_with_items.get_values_(menu_date),
        'menu_date': menu_date,
    })


# Viewsets for REST API

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_fields = {'product_name': ['icontains']}
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSetForSelect2(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializerForSelect2
    filterset_fields = {'product_name': ['icontains']}


class ProductGroupViewSet(viewsets.ModelViewSet):
    queryset = ProductGroup.objects.all()
    serializer_class = ProductGroupSerializer
    filterset_fields = {'group_name': ['icontains']}
    permission_classes = [permissions.IsAuthenticated]


class ProductGroupViewSetForSelect2(viewsets.ModelViewSet):
    queryset = ProductGroup.objects.filter(replacement_for=F('pk'))
    serializer_class = ProductGroupSerializerForSelect2
    filterset_fields = {'group_name': ['icontains']}


class MapViewSet(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    filterset_fields = {'map_number': ['icontains'], 'map_name': ['icontains']}
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        if 'menu_date' in self.request.query_params:
            try:
                datetime.strptime(self.request.query_params['menu_date'], '%Y-%m-%d')
                context['menu_date'] = self.request.query_params['menu_date']
            except ValueError:
                return context
        return context

    def list(self, request, *args, **kwargs):
        self.serializer_class = MapListSerializer
        return super(MapViewSet, self).list(request, *args, **kwargs)

    @action(detail=True, methods=['post'])
    def make_map_clone(self, request, pk=None):
        try:
            parent = self.get_object()
            new_map = Map(map_number=request.data['map_number'], map_name=request.data['map_name'])
            new_map.save()

            for p_in_m in parent.productsinmap_set.all():
                new_p_in_map = ProductsInMap.objects.create(map=new_map, product=p_in_m.product, group=p_in_m.group,
                                                            product_count_gross=p_in_m.product_count_gross,
                                                            product_count_gross_normalize=p_in_m.product_count_gross_normalize,
                                                            dish_category=p_in_m.dish_category)
                new_p_in_map.treatments.add(*p_in_m.treatments.all())
                new_p_in_map.save()
            return Response('Ok', status.HTTP_200_OK)
        except Exception:
            return Response('Bad request', status.HTTP_400_BAD_REQUEST)


class MapViewSetForSelect2(viewsets.ModelViewSet):
    queryset = Map.objects.all()
    serializer_class = MapSerializerForSelect2
    filterset_fields = {'map_name': ['icontains']}


class ProductsInMapViewSet(viewsets.ModelViewSet):
    queryset = ProductsInMap.objects.all()
    serializer_class = ProductsInMapSerializer
    filterset_fields = {'map': ['exact']}
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.serializer_class = ProductsInMapListSerializer
        return super(ProductsInMapViewSet, self).list(request, *args, **kwargs)


class MapsInMenuDayViewSet(viewsets.ModelViewSet):
    queryset = MapsInMenuDay.objects.all()
    serializer_class = MapsInMenuDaySerializer
    permission_classes = [permissions.IsAuthenticated]


class MealTimeViewSet(viewsets.ModelViewSet):
    queryset = MealTime.objects.all()
    serializer_class = MealTimeSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuDayViewSet(viewsets.ModelViewSet):
    queryset = MenuDay.objects.all()
    serializer_class = MenuDaySerializer
    filterset_fields = {'menu_day_date': ['gte', 'lte']}
    permission_classes = [permissions.IsAuthenticated]


class WastageByDateRangeViewSet(viewsets.ModelViewSet):
    queryset = WastageByDateRange.objects.all()
    serializer_class = WastageByDateRangeSerializer
    permission_classes = [permissions.IsAuthenticated]


class TreatmentKindViewSet(viewsets.ModelViewSet):
    queryset = TreatmentKind.objects.all()
    serializer_class = TreatmentKindSerializer
    permission_classes = [permissions.IsAuthenticated]


class DateRangeViewSet(viewsets.ModelViewSet):
    queryset = DateRange.objects.all()
    serializer_class = DateRangeSerializer
    permission_classes = [permissions.IsAuthenticated]


class DishCategoryViewSet(viewsets.ModelViewSet):
    queryset = DishCategory.objects.all()
    serializer_class = DishCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


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


@api_view(['POST'])
def make_map_clone(request):
    try:
        parent = get_object_or_404(Map, pk=request.data['map_parent'])
        new_map = Map(map_number=request.data['map_number'], map_name=request.data['map_name'])
        new_map.save()

        for p_in_m in parent.productsinmap_set.all():
            new_p_in_map = ProductsInMap.objects.create(map=new_map, product=p_in_m.product, group=p_in_m.group,
                                                        product_count_gross=p_in_m.product_count_gross,
                                                        product_count_gross_normalize=p_in_m.product_count_gross_normalize,
                                                        dish_category=p_in_m.dish_category)
            new_p_in_map.treatments.add(*p_in_m.treatments.all())
            new_p_in_map.save()
        return Response('Ok', status.HTTP_200_OK)
    except Exception:
        return Response('Bad request', status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_menus(request):

    if 'menu_day_date_start' in request.query_params and 'menu_day_date_end' in request.query_params:
        f = MenuDayFilter(request.query_params, queryset=MenuDay.objects.all())
        menu_days = f.qs
    else:
        f = MenuDayFilter(request.query_params, queryset=MenuDay.objects.filter(menu_day_date=datetime.now().date()))
        menu_days = f.qs
    maps_in_menu_days_all = MapsInMenuDay.objects.all()
    maps_in_menu_days = maps_in_menu_days_all.filter(menu_day__in=menu_days).distinct()



    if 'menu_day_date_start' in request.query_params and 'menu_day_date_end' in request.query_params:

        date_start_str = request.GET['menu_day_date_start'] if request.GET['menu_day_date_start'] != '' else str(
            datetime.now().date())
        date_end_str = request.GET['menu_day_date_end'] if request.GET['menu_day_date_end'] != '' else str(
            datetime.now().date())

        date_start = datetime.strptime(date_start_str, '%Y-%m-%d').date()
        date_end = datetime.strptime(date_end_str, '%Y-%m-%d').date()
    else:
        date_start = datetime.now().date()
        date_end = datetime.now().date()

    products_group = ProductGroup.objects.all()
    products_group_main = products_group.filter(replacement_for=F('pk'))

    results_maps = {}
    for day in menu_days:
        meals = {}
        for meal in MealTime.objects.all():
            maps_array = []
            maps_ids = [map.map.id for map in maps_in_menu_days]

            for m in maps_in_menu_days_all.filter(menu_day=day, meal_time=meal):
                get_product_group_value_obj = {}
                get_product_count_obj = {}
                for group in products_group_main:
                    products_in_maps = Product.objects.filter(productsinmap__map__in=maps_ids,
                                                              productsinmap__group__replacement_for=group).distinct()
                    get_product_group_value_obj[str(group.id)] = m.map.get_product_group_value(group)

                    for product in products_in_maps:
                        get_product_count_obj[str(product.id)] = m.map.get_product_count(product)

                maps_array.append({'map_id': m.map.id, 'map_name': m.map.map_name, 'get_product_group_value_obj': get_product_group_value_obj,
                                   'get_product_count_obj': get_product_count_obj, 'get_net_weights': m.map.get_net_weights_by_dish_category_(day.menu_day_date),
                                   'get_values': m.map.get_values_(day.menu_day_date)})
                meals[str(meal.id)] = maps_array
        results_maps[str(day.menu_day_date)] = meals

    maps = [map.map.id for map in maps_in_menu_days]

    results_groups_products = []
    for group in products_group_main:
        products_in_maps = Product.objects.filter(productsinmap__map__in=maps, productsinmap__group__replacement_for=group).distinct()
        products = []
        for product in products_in_maps:
            products.append({'product_name': product.product_name, 'product_id': product.id})
        results_groups_products.append({'group_name': group.group_name, 'group_id': group.id, 'norm_per_day': group.norm_per_day, 'products': products})
    return Response({'groups_products': results_groups_products, 'maps': results_maps, 'day_count': relativedelta(date_end, date_start).days + 1,}, status.HTTP_200_OK)






@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_me(request):
    try:
        token = request.META['HTTP_AUTHORIZATION'].split(" ")[1]
        payload = jwt.decode(token, key=settings.SIMPLE_JWT['SIGNING_KEY'], algorithms=['HS256'])
    except jwt.JWTError:
        return Response(status=status.HTTP_403_FORBIDDEN)
    try:
        user_data = User.objects.get(pk=payload['user_id'])
        serializer = UserSerializer(user_data)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return Response(status=status.HTTP_400_BAD_REQUEST)


