from django.shortcuts import render, redirect
from dashboard.models import Book
from .models import Cart, CartItem
from django.http import HttpResponse
from django.shortcuts import get_object_or_404


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, book_id):
    book = Book.objects.get(id=book_id)

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.get(book=book, cart=cart)
        cart_item.quantity += 1
        cart_item.save()

    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            book=book,
            quantity=1,
            cart=cart
        )
        cart_item.save()

    return redirect('cart')


def remove_cart(request, book_id):

    cart = Cart.objects.get(cart_id=_cart_id(request))
    book = get_object_or_404(Book, id=book_id)
    cart_item = CartItem.objects.get(book=book, cart=cart)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()

    else:
        cart_item.delete()
    return redirect('cart')


def delete_cart_items(request, book_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    book = get_object_or_404(Book, id=book_id)
    cart_item = CartItem.objects.get(book=book, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None, delivery_charge=0):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.filter(cart=cart, is_active=True)

        for item in cart_item:
            total += (item.book.price * item.quantity)
            quantity += item.quantity

        if total < 500:
            delivery_charge = 45
        else:
            delivery_charge = 0

        gst = (total * 5)/100

        context = {
            'cart_item': cart_item,
            'total': total,
            'quantity': quantity,
            'delivery_charge': delivery_charge,
            'gst': gst
        }

    except ObjectDoesNotExist:
        pass

    return render(request, 'cart.html', context)
