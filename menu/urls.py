from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_items, name='menu_items'),
    path('products', views.products, name='products'),
    path('product-groups', views.product_groups, name='product_groups'),
    path('maps', views.maps, name='maps'),
    path('maps/<map_id>/items', views.maps_items, name='maps-items'),
    path('menu-day-update-maps/', views.menu_day_update_maps, name='menu_day_update_maps'),
    path('make_map_clone/', views.make_map_clone, name='make_map_clone'),

    # path('card/input', views.card_input, name='card_input'),
    # path('card/<card_id>', views.get_card, name='get_card'),
    # path('card-full/<card_id>', views.get_card_full, name='get_card_full'),
    # path('card/<card_id>/update', views.card_update, name='card_update'),
    #
    # path('clothes', views.clothes_list, name='clothes_list'),
    # path('clothes/input', views.clothes_input, name='clothes_input'),
    # path('clothes/<clothes_id>/update', views.clothes_update, name='clothes_update'),
    # path('clothes/sheet', views.get_sheet, name='clothes_sheet'),
    #
    # path('employees', views.employee_list, name='employee_list'),
    # path('employees/input', views.employee_input, name='employee_input'),
    # path('employees/<employee_id>/<card_id>/update', views.employee_update, name='employee_update'),
    #
    # path('norms', views.norm_list, name='norm_list'),
    # path('norms/<norm_id>/items', views.norm_items, name='norm_items'),
    # # rest-api for making clones based on parent norm
    # path('norms/make-clone/', views.make_cloned_norm, name='norm_make_clone'),
    #
    # path('random', views.get_random_data, name='random'),
    # path('init-dimensions', views.init_dimensions, name='init-dimensions'),
]