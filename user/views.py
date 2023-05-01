from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate
from accounts.models import CustomUser as User
from django.contrib import messages
from django.db.models import Count
from dashboard.models import Book, Image, Author, Book_Category, Review
from order.models import Order, Payment, OrderProduct
from cart.models import Cart, CartItem, Wishlist
from cart.views import _cart_id
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from .models import Address
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from dashboard.forms import Review_form
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm
from django.utils.text import slugify


def home(request):
    books = Book.objects.all()

    return render(request, 'home.html', {'books': books})


def list_book(request,):
    # books = Book.objects.filter(category__cat_name=cat_name)
    sort = request.GET.get('sort')
    if sort == 'latest':
        books = Book.objects.all().order_by('publishing_date')
    elif sort == 'price-low':
        books = Book.objects.all().order_by('price')
    elif sort == 'price-high':
        books = Book.objects.all().order_by('-price')
    elif sort == 'name':
        books = Book.objects.all().order_by('title')
    elif sort == 'default':
        books = Book.objects.all().order_by('id')
    else:
        books = Book.objects.all().order_by('id')

    paginator = Paginator(books, 6)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    book_count = books.count()

    categories = Book_Category.objects.annotate(
        num_books=Count('books')).values('name', 'num_books')

    context = {
        'books': paged_product,
        'category': categories,
        'book_count': book_count

    }
    return render(request, 'books.html', context)


def category_list(request, cat_name, min_price=None, max_price=None):
    if min_price or max_price:

        books = Book.objects.filter(
            categories__name=cat_name, price__gte=min_price, price__lte=max_price)
    else:
        books = Book.objects.filter(categories__name=cat_name)

    category = Book_Category.objects.values(
        'name').annotate(book_count=Count('books'))

    context = {
        'books': books,
        'category': category
    }
    return render(request, 'books.html', context)


def filter_price(request):
    if request.method == 'GET':
        min_price = request.GET['min-price']
        max_price = request.GET['max-price']

        if min_price or max_price:

            books = Book.objects.filter(
                price__gte=min_price, price__lte=max_price)
        else:
            books = Book.objects.all()

    context = {
        'books': books,
    }
    return render(request, 'books.html', context)


def book_details(request, title):

    books = get_object_or_404(Book, title=title)
    in_cart = CartItem.objects.filter(
        cart__cart_id=_cart_id(request), book=books).exists()

    context = {
        'books': books,
        'in_cart': in_cart,
        'form': Review_form,

    }
    return render(request, 'single-product.html', context)


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


@login_required(login_url='login')
def my_account(request):
    user = request.user
    user = User.objects.get(id=user.id)
    address = Address.objects.filter(user=user)
    order_product = OrderProduct.objects.filter(
        user=user).order_by('-created_at')[:5]
    context = {
        'address': address,
        'order_product': order_product
    }

    if request.path == '/my_account/orders':
        return render(request, 'dashboard/my-orders.html', context)

    return render(request, 'dashboard/my-orders.html', context)


@ login_required(login_url='login')
def wishlist(request):
    wishlist = get_object_or_404(Wishlist, user=request.user)
    books = wishlist.book.all()
    context = {
        'books': books
    }
    return render(request, 'dashboard/wishlist.html', context)


@ login_required(login_url='login')
def book_review(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = Review_form(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book-details', title=book.title)
        else:
            form = ReviewForm()
    return HttpResponse('success')


@ login_required(login_url='login')
def password_change_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(
                request, 'Your password was successfully updated!')
            return redirect('home')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'dashboard/change-password.html', {'form': form})


def custom_error_page(request, exception):
    return render(request, '404.html', status=404)
