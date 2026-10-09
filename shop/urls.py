
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    path(
        'products/',
        views.product_list,
        name='product_list'
    ),

    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'product/add/',
        views.product_create,
        name='product_create'
    ),

    path(
        'product/<int:product_id>/edit/',
        views.product_update,
        name='product_update'
    ),

    path(
        'product/<int:product_id>/delete/',
        views.product_delete,
        name='product_delete'
    ),

    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    # Cart URLs
    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/update/<int:product_id>/',
        views.update_cart,
        name='update_cart'
    ),

    path(
        'cart/remove/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

]