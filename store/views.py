from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.db.models import CharField
from django.db.models.functions import Lower

from store.models import Product, Category
from store.forms import AddReviewForm
from store.querysets import get_related_products

CharField.register_lookup(Lower)


def home(request, category_slug=None, page=1):
    category_page = None
    products = None
    search_product = request.GET.get('search')
    search_category = request.GET.get('category') or ''
    
    if search_product:
        products = Product.objects.filter(Q(name__lower__icontains=search_product) |
                                                Q(tags__name__lower__icontains=search_product)).filter(
                                                Q(category__name__exact=search_category)).order_by("-created").distinct()

    elif category_slug != None:
        category_page = get_object_or_404(Category ,slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)
    
    else:
        products = Product.objects.all().filter(available=True)
    
    paginator = Paginator(products, per_page=4, orphans=3)
    page_object = paginator.get_page(page)
    page_object.adjusted_elided_pages = paginator.get_elided_page_range(page, on_each_side=2, on_ends=2)
    
    context = {'category': category_page, 'page_obj': page_object}
    
    return render(request, 'store/home.html', context=context)

def productView(request, category_slug, product_slug):
    try:
        product = Product.objects.get(slug=product_slug, category__slug=category_slug)
        related_products = get_related_products(product)

    except Exception as e:
        raise e

    return render(request, 'store/product.html', {'product':product, "related_products": related_products})

def add_reviewView(request):
    product = None
    next = request.META.get("HTTP_REFERER", None) or "/"
    if request.method == 'POST':
        review_form = AddReviewForm(request.POST)
        product_name = request.POST['product']
        product = Product.objects.get(name=product_name)

        if review_form.is_valid():
            review_form.save()

            return redirect(product)
        
        else:
            errors = review_form.errors
            related_products = get_related_products(product)
            return render(request, 'store/product.html', {'product':product, "related_products": related_products, 'review_errors':errors})
    