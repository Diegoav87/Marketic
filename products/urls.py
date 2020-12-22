from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('create/', views.create_product, name='create'),
    path('user_products/<str:username>/', views.user_product_list, name='user_products'),
    path('update/<int:pk>/', views.update_product, name='update_product'),
    path('delete/<int:pk>/', views.delete_product, name='delete'),
    path('order-create/<int:pk>/', views.create_order, name='create-order'),
    path('customer_order_list/<str:username>/', views.customer_order_list, name='customer_order_list'),
    path('provider_order_list/<str:username>/', views.provider_order_list, name='provider_order_list'),
    path('update-order/<int:pk>/', views.update_order, name='update_order'),
    path('delete-order/<int:pk>/', views.delete_order, name='delete_order'),
] 

