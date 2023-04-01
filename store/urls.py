from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/', views.product, name='product_detail'),
    path('cart/', views.cart, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout_page'),
    path('quick_view/', views.quick_view, name='quick_view'),
]
