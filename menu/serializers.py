from rest_framework import serializers
from .models import Product, ProductGroup, Map, ProductsInMap, MapsInMenuDay,  MealTime, MenuDay, WastageByDateRange


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = '__all__'


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class ProductsInMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInMap
        fields = '__all__'


class MapsInMenuDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MapsInMenuDay
        fields = '__all__'


class MealTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealTime
        fields = '__all__'


class MenuDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuDay
        fields = '__all__'


class WastageByDateRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WastageByDateRange
        fields = '__all__'









