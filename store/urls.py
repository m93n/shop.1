from django.urls import path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<slug:category_slug>', views.home, name='products_by_category'),
    path('product/', views.product, name='product_detail'),
    path('cart/', views.cart, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout_page'),
    path('quick_view/', views.quick_view, name='quick_view'),
]
