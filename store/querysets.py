from store.models import Product

def get_related_products(product_object):
    
    product_tags = product_object.tags.all()
    related_products = Product.objects.filter(tags__in=product_tags).distinct()

    return related_products