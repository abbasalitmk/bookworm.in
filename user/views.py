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
from .forms import AddressForm
from .models import Address
from django.urls import reverse


def home(request):
    books = Book.objects.all().order_by('-publishing_date')
    deal_books = Book.objects.all().order_by('-discount')

    return render(request, 'home.html', {'books': books})


def list_book(request):
    # Get filter parameters
    cat_name = request.GET.get('category')
    min_price = request.GET.get('min-price')
    max_price = request.GET.get('max-price')

    # Get sort parameter
    sort = request.GET.get('sort')

    # Filter books based on category
    if cat_name:
        if min_price or max_price:
            books = Book.objects.filter(
                categories__name=cat_name, price__gte=min_price, price__lte=max_price)
        else:
            books = Book.objects.filter(categories__name=cat_name)
    else:
        if min_price or max_price:
            books = Book.objects.filter(
                price__gte=min_price, price__lte=max_price)
        else:
            books = Book.objects.all()

    # Sort books based on user input
    if sort == 'latest':
        books = books.order_by('publishing_date')
    elif sort == 'price-low':
        books = books.order_by('price')
    elif sort == 'price-high':
        books = books.order_by('-price')
    elif sort == 'name':
        books = books.order_by('title')
    else:
        books = books.order_by('id')

    paginator = Paginator(books, 10)
    page = request.GET.get('page')
    paged_product = paginator.get_page(page)
    book_count = books.count()

    categories = Book_Category.objects.annotate(
        num_books=Count('books')).values('name', 'num_books')

    context = {
        'books': paged_product,
        'category': categories,
        'book_count': book_count,
        'selected_category': cat_name,
        'min_price': min_price,
        'max_price': max_price,
        'selected_sort': sort
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


def book_details(request, slug):

    books = get_object_or_404(Book, slug=slug)
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


@login_required
def create_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            next_url = request.GET.get('next', reverse('view_addresses'))
            return redirect(next_url)
    else:
        form = AddressForm()
    return render(request, 'dashboard/address_create.html', {'form': form})


@login_required
def view_addresses(request):
    addresses = Address.objects.filter(user=request.user)
    context = {'addresses': addresses}
    return render(request, 'dashboard/addresses.html', context)


@login_required
def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('view_addresses')
    else:
        form = AddressForm(instance=address)
    context = {'form': form, 'address_id': address_id}
    return render(request, 'dashboard/edit_address.html', context)


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    address.delete()
    return redirect('view_addresses')
