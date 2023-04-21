from django.shortcuts import get_object_or_404, render
from store import models

def home(request, category_slug=None):
    category_page = None
    products = None
    if category_slug != None:
        category_page = get_object_or_404(models.Category ,slug=category_slug)
        products = models.Product.objects.filter(category=category_page, available=True)
    
    else:
        products = models.Product.objects.all().filter(available=True)
    
    return render(request, 'store\home.html', {'category': category_page, 'products': products})

def product(request, category_slug, product_slug):
    try:
        product = models.Product.objects.get(slug=product_slug, category__slug=category_slug)

    except Exception as e:
        raise e

    return render(request, 'store\product.html', {'product':product})

def cart(request):
    return render(request, 'store\cart.html')

def checkout(request):
    return render(request, 'store\checkout.html')

def quick_view(request, category_slug, product_slug):
    try:
        product = models.Product.objects.get(slug=product_slug, category__slug=category_slug)

    except Exception as e:
        raise e
    
    return render(request, 'store/ajax/shop-product-quick-view.html', {'product':product})