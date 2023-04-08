from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

def home(request):
    return render(request, 'store\home.html')

def product(request):
    return render(request, 'store\product.html')

def cart(request):
    return render(request, 'store\cart.html')

def checkout(request):
    return render(request, 'store\checkout.html')

def quick_view(request):
    return render(request, 'store/ajax/shop-product-quick-view.html')