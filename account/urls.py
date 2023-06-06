from django.urls import path

from account import views

urlpatterns = [
    path('create', views.signupView, name='signup'),
    path('signin', views.signInView, name='signin'),
    path('signout', views.signOutView, name='signout'),
    path('profile', views.user_profile, name='user_profile'),
    path('cart/add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/remove_product/<int:product_id>/', views.cart_remove_product, name='cart_remove_product'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('checkout/', views.checkout, name='checkout_page'),
    path('<int:order_id>/order_complete/', views.shop_order_complete, name='shop_order_complete'),
    path('quick_view/<slug:category_slug>/<slug:product_slug>', views.quick_view, name='quick_view'),
]
