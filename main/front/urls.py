from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('', views.index, name='index'),
    path('category_list/<int:id>', views.category_list, name='category_list'),
    path('product_detail/<str:code>', views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),

]
