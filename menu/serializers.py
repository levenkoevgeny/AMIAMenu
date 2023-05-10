from rest_framework import serializers
from .models import Product, ProductGroup, Map, ProductsInMap, MapsInMenuDay,  MealTime, MenuDay, WastageByDateRange, \
    TreatmentKind, DateRange, DishCategory
from django.contrib.auth.models import User
from datetime import datetime


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


class ProductSerializerForSelect2(serializers.ModelSerializer):
    class Meta:
        model = ProductGroup
        fields = ['id', 'text']


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
    get_net_weights_by_dish_category = serializers.SerializerMethodField()
    get_values = serializers.SerializerMethodField()

    class Meta:
        model = Map
        fields = ['id', 'map_number', 'map_name', 'description', 'get_net_weights_by_dish_category', 'get_values']

    def get_get_net_weights_by_dish_category(self, obj):
        if 'menu_date' in self.context:
            date_time_obj = datetime.strptime(self.context['menu_date'], '%Y-%m-%d')
            return obj.get_net_weights_by_dish_category_(date_time_obj.date())
        return obj.get_net_weights_by_dish_category_()

    def get_get_values(self, obj):
        if 'menu_date' in self.context:
            date_time_obj = datetime.strptime(self.context['menu_date'], '%Y-%m-%d')
            return obj.get_values_(date_time_obj.date())
        return obj.get_values_()


class MapListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Map
        fields = ['id', 'map_number', 'map_name', 'description']


class MapSerializerForSelect2(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ['id', 'text']


class ProductsInMapListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInMap
        fields = ['id', 'product', 'group', 'product_count_gross', 'product_count_gross_normalize', 'dish_category', 'treatments', 'get_net_weight_treatment_array']
        depth = 1


class ProductsInMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductsInMap
        fields = ['id', 'map', 'product', 'group', 'product_count_gross', 'dish_category', 'treatments', 'get_product_name', 'get_group_name']


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


class DishCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCategory
        fields = '__all__'


