from .models import Cart
from menu.models import FoodItem

def get_cart_counter(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            if cart_items:
                for cart_item in cart_items:
                    cart_count += cart_item.quantity
            else:
                cart_count = 0
        except:
            cart_count = 0
    return dict(cart_count=cart_count)

def get_cart_amounts(request):
    subtotal = 0
    tax = float(6.34)
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for item in cart_items:
            fooditem = FoodItem.objects.get(pk=item.fooditem.id)
            subtotal += round(float((fooditem.price * item.quantity)),3)

        tax_amount = round((tax * subtotal) / 100, 2)
        grand_total = round(float(subtotal + tax_amount), 2)
    
    if request.user.is_authenticated:
        return dict(subtotal=subtotal, tax=tax_amount, grand_total=grand_total)
    else:
        return dict(subtotal=subtotal, tax=tax, grand_total=grand_total)