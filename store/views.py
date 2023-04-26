from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
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

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = models.Product.objects.get(id=product_id)
    try:
        cart = models.Cart.objects.get(cart_id=_cart_id(request))
    except models.Cart.DoesNotExist:
        cart = cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    
    try:
        cart_item = models.CartItem.objects.get(product=product, cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1
            cart_item.save()
    except models.CartItem.DoesNotExist:
        cart_item = models.CartItem.objects.create(
            product=product,
            cart=cart,
            quantity = 1,
        )
        cart.save()

    return redirect('cart_detail')

def cart_detail(request, total=0, counter=0, cart_items=None):
    try:
        cart = models.Cart.objects.get(cart_id=_cart_id(request))
        cart_items = models.CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.sale_price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'store\cart.html', dict(cart_items=cart_items, total=total, counter=counter))

def checkout(request):
    return render(request, 'store\checkout.html')

def quick_view(request, category_slug, product_slug):
    try:
        product = models.Product.objects.get(slug=product_slug, category__slug=category_slug)

    except Exception as e:
        raise e
    
    return render(request, 'store/ajax/shop-product-quick-view.html', {'product':product})