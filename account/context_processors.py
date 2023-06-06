from account.models import Cart, CartItem
from account.views import _cart_id

def cart_item_counter_and_total(request):
    cart=None
    item_count = 0
    total=0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.get(cart_id = _cart_id(request))
            cart_items = CartItem.objects.all().filter(cart=cart)
            for cart_item in cart_items:
                item_count += cart_item.quantity
                total += (cart_item.product.sale_price * cart_item.quantity)
            
        except Cart.DoesNotExist:
            item_count = 0
    
    return dict(cart=cart, item_count=item_count, total=total)
