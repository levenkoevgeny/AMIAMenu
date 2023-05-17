from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from menu import views


router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'products-select2', views.ProductViewSetForSelect2)
router.register(r'product-groups', views.ProductGroupViewSet)
router.register(r'product-groups-select2', views.ProductGroupViewSetForSelect2)
router.register(r'maps', views.MapViewSet)
router.register(r'maps-select2', views.MapViewSetForSelect2)
router.register(r'products-in-map', views.ProductsInMapViewSet)
router.register(r'maps-in-menu', views.MapsInMenuDayViewSet)
router.register(r'meal-times', views.MealTimeViewSet)
router.register(r'menu-days', views.MenuDayViewSet)
router.register(r'wastage-by-date-range', views.WastageByDateRangeViewSet)
router.register(r'treatment-kinds', views.TreatmentKindViewSet)
router.register(r'date-ranges', views.DateRangeViewSet)
router.register(r'dish-categories', views.DishCategoryViewSet)


urlpatterns = [
    path('api/users/me/', views.get_me),
    path('api/menus/', views.get_menus),
    path('api/', include(router.urls)),
    # path('', RedirectView.as_view(url='/menu'), name="redirect-to-menu"),
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('menu/', include('menu.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
