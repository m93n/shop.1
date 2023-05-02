from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.conf import settings
import stripe
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
        cart = models.Cart.objects.create(
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

def cart_remove(request, product_id):
    cart = models.Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(models.Product, id=product_id)
    cart_item = models.CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart_detail')

def cart_remove_product(request, product_id):
    cart = models.Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(models.Product, id=product_id)
    cart_item = models.CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def checkout(request):

    total=0
    order_details = None


    cart = models.Cart.objects.get(cart_id = _cart_id(request))
    cart_items = models.CartItem.objects.filter(cart=cart, active=True)
    for cart_item in cart_items:
        total += (cart_item.product.sale_price * cart_item.quantity)
    
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = 'Store - New Order'
    data_key = settings.STRIPE_PUBLISH_KEY

    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            email = request.POST['stripeEmail']
            billingName = request.POST['stripeBillingName']
            billingAddress1 = request.POST['stripeBillingAddressLine1']
            billingCity = request.POST['stripeBillingAddressCity']
            billingPostcode = request.POST['stripeBillingAddressZip']
            billingCountry = request.POST['stripeBillingAddressCountryCode']
            shippingName = request.POST['stripeShippingName']
            shippingAddress1 = request.POST['stripeShippingAddressLine1']
            shippingCity = request.POST['stripeShippingAddressCity']
            shippingPostcode = request.POST['stripeShippingAddressZip']
            shippingCountry = request.POST['stripeShippingAddressCountryCode']
            customer = stripe.Customer.create(
                email=email,
                source=token
            )
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency='usd',
                description=description,
                customer=customer.id
            )

            # Creating the order
            try:
                order_details = models.Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry
                )
                order_details.save()
                for order_item in cart_items:
                    or_item = models.OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.sale_price,
                        order=order_details
                    )
                    or_item.save()

                    # reduce stock
                    products = models.Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()

                return redirect('shop_order_complete', order_details.id)
            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e

    return render(request, 'store\checkout.html', dict(cart_items=cart_items, order=order_details, data_key=data_key, stripe_total=stripe_total, description=description))

def shop_order_complete(request, order_id):
    if order_id:
        order = get_object_or_404(models.Order, id=order_id)
        order_items = models.OrderItem.objects.filter(order=order)

    return render(request, 'store\shop-order-complete.html', dict(order=order, order_items=order_items))

def quick_view(request, category_slug, product_slug):
    try:
        product = models.Product.objects.get(slug=product_slug, category__slug=category_slug)

    except Exception as e:
        raise e
    
    return render(request, 'store/ajax/shop-product-quick-view.html', {'product':product})