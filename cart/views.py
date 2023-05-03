from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import math
from dashboard.models import Book, Variation, Coupon, BookVariation
from .models import Cart, CartItem, Wishlist
from user.models import Address
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, book_id):
    user = request.user
    book = Book.objects.get(id=book_id)

    if user.is_authenticated:
        variations = []
        if request.method == 'POST':

            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = BookVariation.objects.get(
                        variation_type__iexact=value,
                        book__id=book_id
                    )
                    variations.append(variation)
                except BookVariation.DoesNotExist:
                    pass

        cart_item = None
        for item in user.cartitem_set.filter(book=book, is_active=True):
            if set(item.variation.all()) == set(variations):
                cart_item = item
                cart_item.quantity += 1
                cart_item.save()
                break

        if not cart_item:
            cart_item = CartItem.objects.create(
                book=book, user=user, quantity=1)
            cart_item.variation.add(*variations)
            cart_item.save()

        return redirect('cart')

    else:
        variations = []
        if request.method == 'POST':
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = BookVariation.objects.get(
                        variation_type__iexact=value,
                        book__id=book_id
                    )
                    variations.append(variation)
                except BookVariation.DoesNotExist:
                    pass

        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
            cart.save()

        cart_item = None
        for item in cart.cartitem_set.filter(book=book, is_active=True):
            if set(item.variation.all()) == set(variations):
                cart_item = item
                cart_item.quantity += 1
                cart_item.save()
                break

        if not cart_item:
            cart_item = CartItem.objects.create(
                book=book, cart=cart, quantity=1)
            cart_item.variation.add(*variations)
            cart_item.save()

        return redirect('cart')


def increment_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


def decrement_cart_item(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def delete_Cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None, delivery_charge=0):
    context = {}
    variation_price = 0
    paperback_price = 0

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(
                user=request.user, is_active=True)

        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_item:
            if item.variation:
                try:
                    variation = item.variation.get()
                    price = variation.price
                    variation_price += (price * item.quantity)
                # variation_price = item.variation.price
                # cart_total += (book_price * item.quantity)
                except:

                    paperback_price += (item.book.price * item.quantity)

            quantity += item.quantity

        total = variation_price + paperback_price

        if total < 500:
            delivery_charge = 45
        else:
            delivery_charge = 0

        gst = (total * 5)/100
        grand_total = math.ceil(total+gst+delivery_charge)

        context = {
            'cart_item': cart_item,
            'total': total,
            'quantity': quantity,
            'delivery_charge': delivery_charge,
            'gst': gst,
            'grand_total': grand_total
        }

    except Cart.DoesNotExist:
        print('no cart')

    return render(request, 'cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None, delivery_charge=0, sub_total=0):
    address = Address.objects.filter(user=request.user)
    cart_item = CartItem.objects.filter(user=request.user)
    if cart_item.count() <= 0:
        return redirect('cart')

    context = {}
    variation_price = 0
    paperback_price = 0

    try:
        user = request.user
        cart_item = CartItem.objects.filter(user=user, is_active=True)

        for item in cart_item:
            if item.variation:
                try:
                    variation = item.variation.get()
                    price = variation.price
                    variation_price += (price * item.quantity)
                # variation_price = item.variation.price
                # cart_total += (book_price * item.quantity)
                except:

                    paperback_price += (item.book.price * item.quantity)
            quantity += item.quantity
        total = variation_price + paperback_price

        if total < 500:
            delivery_charge = 45
        else:
            delivery_charge = 0

        gst = (total * 5)/100
        grand_total = math.ceil(total+gst+delivery_charge)

        try:
            coupon_discount = request.session.get('discount')
            grand_total = grand_total-coupon_discount
        except:
            pass

        context = {
            'cart_item': cart_item,
            'total': total,
            'quantity': quantity,
            'delivery_charge': delivery_charge,
            'gst': gst,
            'grand_total': grand_total,
            'sub_total': sub_total,
            'addresses': address,
            'coupon_discount': coupon_discount
        }

    except Cart.DoesNotExist:
        pass

    return render(request, 'checkout.html', context)


@login_required(login_url='login')
def order_summary(request, total=0, quantity=0, cart_items=None, delivery_charge=0, sub_total=0):
    context = {}

    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)

    for item in cart_item:
        total += (item.book.price * item.quantity)
        quantity += item.quantity
        sub_total += item.book.price

    if total < 500:
        delivery_charge = 45
    else:
        delivery_charge = 0

    gst = (total * 5)/100
    grand_total = total+gst+delivery_charge

    cart_count = cart_item.count()

    if cart_count <= 0:
        return redirect('checkout')

    order_number = ''

    context = {
        'order_item': Order.objects.filter(user=current_user, is_ordered=False, order_number=order_number),
        'cart_item': cart_item,
        'total': total,
        'quantity': quantity,
        'delivery_charge': delivery_charge,
        'gst': gst,
        'grand_total': grand_total,
        'sub_total': sub_total,

        'coupon_discount': coupon_discount
    }

    return render(request, 'order_summary.html', context)


@ login_required(login_url='login')
def apply_coupon(request):
    try:
        del request.session['discount']
    except:
        pass

    coupon_text = request.GET['coupon-text']
    try:
        if (coupon_text):
            coupon = Coupon.objects.get(coupon_text=coupon_text)
            discount = coupon.discount_amount
            request.session['discount'] = discount
            messages.success(request, 'Coupon Applied')
        else:
            messages.error(request, 'Invalid Coupon')
            discount = 0

    except Coupon.DoesNotExist:
        messages.error(request, 'Invalid Coupon')

    return redirect(reverse('checkout'))


@login_required(login_url='login')
def add_to_wishlist(request, books_id):
    user = request.user
    book = Book.objects.get(id=books_id)

    try:
        wishlist = Wishlist.objects.get(user=user)
        if wishlist.book.filter(id=book.id).exists():
            messages.error(request, 'Book already in wishlist')
        else:
            wishlist.book.add(book)
            messages.success(request, 'Added to wishlist')
    except Wishlist.DoesNotExist:
        wishlist = Wishlist.objects.create(user=user)
        created = True
        wishlist.book.add(book)
        messages.success(request, 'Added to wishlist')
    return redirect('book-details', slug=book.slug)


@ login_required(login_url='login')
def remove_from_wishlist(request, book_id):
    book = Book.objects.get(id=book_id)
    wishlist = Wishlist.objects.get(user=request.user)
    wishlist.book.remove(book)
    messages.warning(request, "Book removed from wishlist")
    return redirect('wishlist')


@ login_required(login_url='login')
def move_to_cart(request, book_id):
    wishlist = Wishlist.objects.get(user=request.user)
    book = wishlist.book.get(id=book_id)
    wishlist.book.remove(book)
    add_cart(request, book_id)
    return redirect('cart')
