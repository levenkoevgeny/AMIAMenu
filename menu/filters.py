import django_filters
from django import forms

from .models import MenuDay, ProductGroup, Product, Map

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class MenuDayFilter(django_filters.FilterSet):
    menu_day_date_start = django_filters.DateFilter(widget=myDateInput, field_name="menu_day_date", lookup_expr="gte")
    menu_day_date_end = django_filters.DateFilter(widget=myDateInput, field_name="menu_day_date", lookup_expr="lte")

    class Meta:
        model = MenuDay
        fields = '__all__'


class ProductGroupFilter(django_filters.FilterSet):
    group_name = django_filters.CharFilter(field_name="group_name", lookup_expr='icontains')

    class Meta:
        model = ProductGroup
        fields = '__all__'


class ProductFilter(django_filters.FilterSet):
    product_name = django_filters.CharFilter(field_name="product_name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = '__all__'


class MapFilter(django_filters.FilterSet):
    map_number = django_filters.CharFilter(field_name="map_number", lookup_expr='icontains')
    map_name = django_filters.CharFilter(field_name="map_name", lookup_expr='icontains')

    class Meta:
        model = Map
        fields = '__all__'