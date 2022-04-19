from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from rest_framework import routers

from menu import views


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'product-groups', views.ProductGroupViewSet)
router.register(r'maps', views.MapViewSet)
router.register(r'products-in-map', views.ProductsInMapViewSet)
router.register(r'maps-in-menu', views.MapsInMenuDayViewSet)
router.register(r'meal-times', views.MealTimeViewSet)
router.register(r'menu-days', views.MenuDayViewSet)
router.register(r'wastage-by-date-range', views.WastageByDateRangeViewSet)


urlpatterns = [
    path('', RedirectView.as_view(url='/menu'), name="redirect-to-menu"),
    path('admin/', admin.site.urls),
    path('menu/', include('menu.urls')),
    path('api/', include(router.urls)),
]
