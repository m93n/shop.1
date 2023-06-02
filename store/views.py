from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
import stripe
from store import models
from store.forms import SignUpForm, SignInForm, UserUpdateForm, ProfileUpdateForm, CartItemForm
from store.querysets import get_related_products

from django.db.models import CharField
from django.db.models.functions import Lower

CharField.register_lookup(Lower)


def home(request, category_slug=None, page=1):
    category_page = None
    products = None
    search_product = request.GET.get('search')
    search_category = request.GET.get('category') or ''
    
    if search_product:
        products = models.Product.objects.filter(Q(name__lower__icontains=search_product) |
                                                Q(tags__name__lower__icontains=search_product)).filter(
                                                Q(category__name__exact=search_category)).order_by("-created").distinct()

    elif category_slug != None:
        category_page = get_object_or_404(models.Category ,slug=category_slug)
        products = models.Product.objects.filter(category=category_page, available=True)
    
    else:
        products = models.Product.objects.all().filter(available=True)
    
    paginator = Paginator(products, per_page=4, orphans=3)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=2, on_ends=2)
    
    context = {'category': category_page, 'page_obj': page_object}
    
    return render(request, 'store/home.html', context=context)

def productView(request, category_slug, product_slug):
    try:
        product = models.Product.objects.get(slug=product_slug, category__slug=category_slug)
        related_products = get_related_products(product)

    except Exception as e:
        raise e

    return render(request, 'store/product.html', {'product':product, "related_products": related_products})

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

    if request.method == "POST":
        cart_item_form = CartItemForm(request.POST, instance=product)

        if cart_item_form.is_valid():
            cart_item_form.save(cart=cart)
        
        else:
            related_products = get_related_products(product)
            return render(request, 'store/product.html', {'product':product, "related_products": related_products, 'form':cart_item_form})


    else:
        choosen_informations = dict()
        for info in models.AdditionalInformation.objects.filter(product=product):
            info_value = info.additionalinformationvalue_set.filter(default=True)[0]
            choosen_informations[info.name]= info_value
        try:
            cart_item = models.CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity < cart_item.product.stock:
                cart_item.quantity += 1
                choosen_informations = choosen_informations
                cart_item.save()
        except models.CartItem.DoesNotExist:
            cart_item = models.CartItem.objects.create(
                product=product,
                cart=cart,
                quantity = 1,
                choosen_informations = choosen_informations
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

    return render(request, 'store/cart.html', dict(cart_items=cart_items, total=total, counter=counter))

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
                        choosen_informations=order_item.choosen_informations,
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

    return render(request, 'store/checkout.html', dict(cart_items=cart_items, order=order_details, data_key=data_key, stripe_total=stripe_total, description=description))

def shop_order_complete(request, order_id):
    if order_id:
        order = get_object_or_404(models.Order, id=order_id)
        order_items = models.OrderItem.objects.filter(order=order)

    return render(request, 'store/shop-order-complete.html', dict(order=order, order_items=order_items))

def quick_view(request, category_slug, product_slug):
    try:
        product = models.Product.objects.get(slug=product_slug, category__slug=category_slug)

    except Exception as e:
        raise e
    
    return render(request, 'store/ajax/shop-product-quick-view.html', {'product':product})

def signupView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Customer')
            customer_group.user_set.add(signup_user)
            login(request, signup_user)
        
    else:
        form = SignUpForm()

    return render(request, 'store/SignUp.html', {'form': form})

def signInView(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')

            else:
                return redirect('signup')
    else:
        form = SignInForm()
    
    return render(request, 'store/SignIn.html', {'form': form})

def signOutView(request):
    logout(request)

    return redirect('signin')

@login_required
def user_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, 'Your profile is updated successfully')

            return redirect(to='user_profile')
    
    return render(request, 'store/user-profile.html', dict(user_form=user_form, profile_form=profile_form))
