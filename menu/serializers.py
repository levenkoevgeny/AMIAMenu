from rest_framework import serializers
from .models import Product, ProductGroup, Map, ProductsInMap, MapsInMenuDay,  MealTime, MenuDay, WastageByDateRange, \
    TreatmentKind, DateRange
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class WastageByDateRangeSerializer(serializers.ModelSerializer):
    treatment_kind = serializers.ReadOnlyField(source='treatment_kind.id')
    date_range = serializers.ReadOnlyField(source='date_range.id')

    class Meta:
        model = WastageByDateRange
        fields = ['id', 'percent', 'treatment_kind', 'date_range']


class ProductSerializer(serializers.ModelSerializer):
    wastage_list = WastageByDateRangeSerializer(source='wastagebydaterange_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'energy_value', 'proteins', 'fats', 'carbohydrates', 'wastage_list']


class ProductGroupManySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductGroup
        fields = ['id', 'group_name', 'norm_per_day', 'in_count', 'replacement_for']


class ProductGroupSerializer(serializers.ModelSerializer):
    replacements = ProductGroupManySerializer(source='get_replacements', many=True, read_only=True)

    class Meta:
        model = ProductGroup
        fields = ['id', 'group_name', 'norm_per_day', 'replacement_for', 'in_count', 'replacements']


class ProductGroupSerializerForSelect2(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['id', 'text']


class DateRangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DateRange
        fields = ['id', 'date_from', 'date_till', 'get_formatted_data']


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class MapSerializerForSelect2(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'text']


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


class TreatmentKindSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentKind
        fields = '__all__'





