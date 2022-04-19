from django.forms import ModelForm
from .models import Product, Map, ProductsInMap, MapsInMenuDay,  MealTime, MenuDay
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type': 'date'})


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class MapForm(ModelForm):
    class Meta:
        model = Map
        fields = '__all__'