from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from accounts.models import CustomUser as User
from django.contrib import messages
from django.db.models import Count
from dashboard.models import Book, Image, Author, Category
from cart.models import Cart, CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger


def home(request):
    books = Book.objects.all()

    return render(request, 'home.html', {'books': books})


def list_book(request,):
    # books = Book.objects.filter(category__cat_name=cat_name)
    books = Book.objects.all().order_by('id')
    paginator = Paginator(books, 6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)

    category = Category.objects.values(
        'cat_name').annotate(book_count=Count('book'))

    context = {
        'books': paged_product,
        'category': category
    }
    return render(request, 'books.html', context)


def category_list(request, cat_name, min_price=None, max_price=None):
    if min_price and max_price:

        books = Book.objects.filter(
            category__cat_name=cat_name, price__gte=min_price, price__lte=max_price)
    else:
        books = Book.objects.filter(category__cat_name=cat_name)

    category = Category.objects.values(
        'cat_name').annotate(book_count=Count('book'))

    context = {
        'books': books,
        'category': category
    }
    return render(request, 'books.html', context)


def book_details(request, title):
    books = Book.objects.get(title=title)
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), book=books).exists()

    context = {
        'books': books,
        'in_cart': in_cart,

    }
    return render(request, 'single-product.html', context)


@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')


@ login_required(login_url='login')
def changePassword(request, id):
    if request.method == 'POST':
        user = User.objects.get(id=id)
        old_password = request.POST['current-pwd']
        new_password = request.POST['new-pwd']
        confirm_pwd = request.POST['confirm-pwd']

        if old_password == '' or new_password == '' or confirm_pwd == '':
            messages.error(request, "Fields can't be blank")
            return redirect('new_password')

        if not authenticate(email=user.email, password=old_password):
            messages.error(request, 'Current password is not valid')
        else:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            messages.success(request, 'Password reset successfully')
            return redirect('profile')

    return render(request, 'change-pwd.html')


def searchBook(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            books = Book.objects.filter(title__icontains=keyword)
    context = {
        'books': books,

    }
    return render(request, 'books.html', context)
