from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from store.models import Product, Variation
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# Create your views here.
def _cart_id(request):
    cart = request.session.session_key

    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request,product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_values__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product = product,
                user=current_user
            )
            '''
            existing variations
            current variations(product_variation)
            item_id
            '''
            existing_variations_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variations_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user=current_user
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart:cart')
    else:
        product_variation = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_values__iexact=value)
                    product_variation.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(
                product = product,
                cart = cart
            )
            '''
            existing variations
            current variations(product_variation)
            item_id
            '''
            existing_variations_list = []
            id = []
            for item in cart_item:
                existing_variations = item.variations.all()
                existing_variations_list.append(list(existing_variations))
                id.append(item.id)

            if product_variation in existing_variations_list:
                index = existing_variations_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()

            else:
                item = CartItem.objects.create(product=product, quantity=1, cart=cart)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()
        return redirect('cart:cart')

def decrement_cart_item(request,product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id = cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart:cart')

def remove_from_cart(request, product_id,cart_item_id):
    product = Product.objects.get(id = product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id = cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(cart=cart, product=product, id=cart_item_id)
    cart_item.delete()
    return redirect('cart:cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0,
        grand_total = 0,
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (total * 7)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    
    context={
        'cart_items'    :cart_items,
        'total'         :total,
        'quantity'      :quantity,
        'tax'           :tax,
        'grand_total'   :grand_total
    }
    return render(request, 'store/cart.html', context)

@login_required
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0,
        grand_total = 0,
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            quantity += cart_item.quantity
        tax = (total * 7)/100
        grand_total = total + tax

    except ObjectDoesNotExist:
        pass
    
    context = {
        'cart_items'    :cart_items,
        'total'         :total,
        'quantity'      :quantity,
        'tax'           :tax,
        'grand_total'   :grand_total
    }
    return render(request, 'store/checkout.html', context)