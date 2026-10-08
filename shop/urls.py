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
]