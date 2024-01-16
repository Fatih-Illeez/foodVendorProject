from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from vendor.models import Vendor
from menu.models import Category , FoodItem
from django.db.models import Prefetch
from .models import Cart
from .context_processors import get_cart_counter, get_cart_amounts
from django.contrib.auth.decorators import login_required
from orders.forms import OrderForm
from .models import Cart
from accounts.models import UserProfile



def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors' : vendors,
        'vendor_count' : vendor_count,
    }
    return render(request, 'marketplace/listings.html', context)

def vendor_detail(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'fooditems',
            queryset=FoodItem.objects.filter(is_available=True)
        )
    )

    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None

    context = {
        'vendor' : vendor,
        'categories' : categories,
        'cart_items' : cart_items
    }
    return render(request, 'marketplace/vendor_detail.html', context)

def add_to_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user already added that food to cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    chkCart.quantity += 1
                    chkCart.save()
                    return JsonResponse({'status': 'Success', 'message': 'Increased the quantity', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    chkCart = Cart.objects.create(user=request.user, fooditem=fooditem, quantity=1)
                    return JsonResponse({'status': 'Success', 'message': 'Cart added', 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Log in to continue'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Login required'})
    
def decrease_cart(request, food_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            #check if the food item exists
            try:
                fooditem = FoodItem.objects.get(id=food_id)
                #check if the user already added that food to cart
                try:
                    chkCart = Cart.objects.get(user=request.user, fooditem=fooditem)
                    if chkCart.quantity > 1:
                        chkCart.quantity -= 1
                        chkCart.save()
                    else:
                        chkCart.delete()
                        chkCart.quantity = 0
                    # decrease quantity
                    return JsonResponse({'status': 'Success', 'message': 'Decreased the quantity' , 'cart_counter': get_cart_counter(request), 'qty': chkCart.quantity, 'cart_amount': get_cart_amounts(request)})
                except:
                    return JsonResponse({'status': 'Failed', 'message': 'You do not have this item in your cart'})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Log in to continue'})
    else:
        return JsonResponse({'status': 'login_required', 'message': 'Login required'})
    

@login_required(login_url='login')
def cart(request):
    cart_items = Cart.objects.filter(user=request.user).order_by('created_at')
    context = {
        'cart_items' : cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def delete_cart(request, cart_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            try:
                #check if the cart item exists
                cart_item = Cart.objects.get(user=request.user, id=cart_id)
                if cart_item:
                    cart_item.delete()
                    return JsonResponse({'status' : 'Success', 'message' : 'Cart item has been deleted!', 'cart_counter': get_cart_counter(request), 'cart_amount': get_cart_amounts(request)})
            except:
                return JsonResponse({'status': 'Failed', 'message': 'Cart item does not exist!'})
        else:
            return JsonResponse({'status': 'Failed', 'message': 'Log in to continue'}) 
        

def search(request):
    print(request)
    address = request.GET['address']
    latitude = request.GET['lat']
    longitude = request.GET['lng']
    radius = request.GET['radius']
    r_name = request.GET['rest_name']

    return render(request, 'marketplace/listings.html')


@login_required(login_url='login')
def checkout(request):
    cart_item = Cart.objects.filter(user=request.user).order_by('created_at')
    cart_count = cart_item.count()
    if cart_count <= 0:
        return redirect('marketplace')
    user_profile = UserProfile.objects.get(user=request.user)
    default_values = {
        'first_name' : request.user.first_name,
        'last_name' : request.user.last_name,
        'phone' : request.user.phone_number,
        'email' : request.user.email,
        'address' : user_profile.address,
        'country' : user_profile.country,
        'state' : user_profile.state,
        'city' : user_profile.city,
        'pin_code' : user_profile.pin_code,
    }
    form = OrderForm(initial=default_values)
    context = {
        'form' : form,
        'cart_items' : cart_item,
        'cart_count' : cart_count,
    }
    return render(request, 'marketplace/checkout.html', context)