from django.shortcuts import render

def home(request):
    return render(request, 'store\home.html')

def product(request):
    return render(request, 'store\product.html')

def cart(request):
    return render(request, 'store\cart.html')

