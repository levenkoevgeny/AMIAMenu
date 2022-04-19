from django.contrib import admin
from .models import Map, MealTime, MenuDay, ProductGroup, Product, ProductsInMap, MapsInMenuDay, DishCategory, \
    TreatmentKind, DateRange, WastageByDateRange, WastageByHeatTreatment

admin.site.register(Map)
admin.site.register(MealTime)
admin.site.register(MenuDay)
admin.site.register(ProductGroup)
admin.site.register(Product)
admin.site.register(ProductsInMap)
admin.site.register(MapsInMenuDay)
admin.site.register(DishCategory)
admin.site.register(TreatmentKind)
admin.site.register(DateRange)
admin.site.register(WastageByDateRange)
admin.site.register(WastageByHeatTreatment)
