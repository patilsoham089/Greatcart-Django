from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from store.models import Product, Variation
from .models import Cart,CartItem

# Create your views here.

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request,product_id):
    
    product = Product.objects.get(id=product_id)
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product,variation_category__iexact=key,variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
        cart.save()
    is_cart_item_exist = CartItem.objects.filter(product=product,cart=cart).exists()
    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product,cart=cart)
        #existing variation -> database
        #current variation -> product variation
        # item id -> database
        ex_var_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            ex_var_list.append(list(existing_variation))
            id.append(item.id)
            
        if product_variation in ex_var_list:
            #increase the quantity by one
            index = ex_var_list.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product,id=item_id)
            item.quantity += 1
            item.save()
            
        else:
            item = CartItem.objects.create(product=product,quantity=1,cart=cart)
            if len(product_variation) > 0:
                item.variation.clear()
                item.variation.add(*product_variation)
            item.save()
        
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variation)
        cart_item.save()
    
    return redirect('cart')
    



def remove_item(request, product_id, cart_item_id):
        # Get the cart using the cart_id
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        # Get the cart item using product_id
        
        
        # Decrease the quantity of the cart item
        try:
            cart_item = CartItem.objects.get(product=product,cart=cart, id=cart_item_id)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                # If quantity is 1, remove the item from the cart
                cart_item.delete()
        except:
            pass
    
        return redirect('cart')

def delete_item(request, product_id, cart_item_id):
    cart = get_object_or_404(Cart, cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    
    # Get the CartItem based on the cart and product_id
    cart_item = get_object_or_404(CartItem, cart=cart, product=product, id = cart_item_id)
    
    # Delete the CartItem
    cart_item.delete()
    
    # Redirect back to the cart view
    return redirect('cart')

def view_cart(request):
    return redirect('cart')
    

def cart(request, total=0, quantity=0, cart_items=None):
    final = 0
    g_total = 0
    tax = 0  # Example tax amount
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        
        g_total = total  # Calculate the grand total
        tax = int(.02*(g_total))
        final = g_total+tax

    except Cart.DoesNotExist:
        # Handle the case where the cart does not exist
        cart_items = []
        g_total = 0  # Ensure g_total remains 0 if cart doesn't exist
    
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'g_total': g_total,  # Pass g_total to the template
        'tax': tax,  # Pass tax to the template
        'final':final,
    }
    
    return render(request, 'store/cart.html', context)



