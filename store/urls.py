from django.urls import path, re_path
from store import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:page>', views.home, name='products_by_page'),
    path('category/<slug:category_slug>', views.home, name='products_by_category'),
    path('category/<slug:category_slug>/<int:page>', views.home, name='products_by_category_by_page'),
    path('category/<slug:category_slug>/<slug:product_slug>', views.productView, name='product_detail'),
    path('add_review/', views.add_reviewView, name='add_review'),
]
