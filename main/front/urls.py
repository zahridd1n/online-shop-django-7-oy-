from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('', views.index, name='index'),
    path('category_list/<int:id>', views.category_list, name='category_list'),
    path('product_detail/<str:code>', views.product_detail, name='product_detail'),

    # --cart
    path('cart_list/', views.cart_list, name='cart_list'),
    path('cart_active/', views.active_cart, name='cart_active'),
    path('cart/<str:code>/', views.cart_detail, name='cart'),
    path('cart_product_delete/<int:id>/', views.cart_product_delete, name='cart_product_delete'),
    path('add_cart_product/<str:code>/', views.add_cart_product, name='add_cart_product'),
    path('nima/<int:id>/', views.nima, name='nima'),
    path('product_order', views.product_order, name='product_order'),

    # --wishlist
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist_delete/<str:code>/', views.wishlist_delete, name='wishlist_delete'),
    path('wishlist_add/<str:code>/', views.wishlist_add, name='wishlist_add'),


]
