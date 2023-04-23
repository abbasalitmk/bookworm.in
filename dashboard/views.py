from django.shortcuts import render, redirect
from .models import Book, Book_Category, BookVariation, Author, Image, Coupon
from order.models import Order, OrderProduct, Payment
from .forms import BookForm, CategoryForm, CouponForm
from accounts.models import CustomUser as User
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.db.models import Q

from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime, timedelta
from django.http import HttpResponse
from .forms import GetYear
from django.contrib import messages


def dashboard_home(request):

    orders = Order.objects.all()
    total_order = orders.count()
    payment = Payment.objects.filter(status='Success')
    total_customers = orders.values('user').distinct().count()

    revenue = 0

    for item in payment:
        revenue += item.amount_paid

    context = {
        'orders': orders,
        'total_order': total_order,
        'revenue': revenue,
        'total_customers': total_customers
    }
    return render(request, 'dashboard/index.html', context)


def product_list(request):
    books = Book.objects.all().order_by('-id')

    if request.method == 'GET':

        sort = request.GET.get('sortby')
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

    context = {
        'books': books
    }
    return render(request, 'dashboard/product_list.html', context)


def search_books(request):

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            books = Book.objects.filter(title__icontains=keyword)

    context = {
        'books': books
    }
    return render(request, 'dashboard/product_list.html', context)


def product_grid(request):
    books = Book.objects.all().order_by('-id')
    context = {
        'books': books
    }
    return render(request, 'dashboard/product_grid.html', context)


def orders(request):
    status_choices = Order.STATUS
    form = GetYear()

    if request.method == 'GET':
        sortby = request.GET.get('sortby')
        if sortby == 'price':
            orders = Order.objects.order_by('-order_total')
        elif sortby == 'default':
            return redirect('orders')
        elif sortby:
            orders = Order.objects.filter(status=sortby)
        else:
            orders = Order.objects.all()

    context = {
        'orders': orders,
        'form': form,
        'status_choices': status_choices
    }
    return render(request, 'dashboard/orders.html', context)


def payment(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }

    return render(request, 'dashboard/payment.html', context)


def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            # Create the Book object
            book = form.save()

            # Create the BookVariation object
            variation_type = form.cleaned_data['variation_type']
            variation_price = form.cleaned_data['variation_price']
            BookVariation.objects.create(
                book=book,
                variation_type=variation_type,
                price=variation_price
            )

            # Create the Author object
            author_name = form.cleaned_data['author_name']
            Author.objects.create(
                book=book,
                name=author_name
            )

            # Create the Image object
            image = form.cleaned_data['image']
            Image.objects.create(
                book=book,
                url=image
            )

            # Add the categories to the book
            categories = form.cleaned_data['categories']
            book.categories.set(categories)

            # Redirect to the book detail page
            return redirect('books_list')
    else:
        form = BookForm()
    return render(request, 'dashboard/add_book.html', {'book_form': form})


def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    categories = Book_Category.objects.all()

    selected_categories = book.categories.values_list('id', flat=True)

    image_url = book.image.first().url.url
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # Save the changes to the book
            book = form.save()

            # Update the BookVariation object
            variation_type = form.cleaned_data['variation_type']
            variation_price = form.cleaned_data['variation_price']
            # assuming there is only one BookVariation object per Book
            book_variation = book.book_variation.first()
            book_variation.variation_type = variation_type
            book_variation.price = variation_price
            book_variation.save()

            # Update the Author object
            author_name = form.cleaned_data['author_name']
            # assuming there is only one Author object per Book
            author = book.author.first()
            author.name = author_name
            author.save()

            # Update the Image object
            image = form.cleaned_data['image']
            # assuming there is only one Image object per Book
            book_image = book.image.first()
            book_image.url = image
            book_image.save()

            # Update the categories of the book
            categories = form.cleaned_data['categories']
            book.categories.set(categories)

            # Redirect to the book detail page
            return redirect('books_list')
    else:

        initial_values = {
            'variation_type': book.book_variation.first().variation_type,
            'variation_price': book.book_variation.first().price,
            'author_name': book.author.first().name,
            'categories': selected_categories
        }
        form = BookForm(instance=book, initial=initial_values)

    context = {
        'book_form': form,
        'book': book,
        'image': image_url
    }
    return render(request, 'dashboard/edit_book.html', context)


def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('books_list')


def order_details(request, order_number):
    order = Order.objects.filter(order_number=order_number)
    order_products = OrderProduct.objects.filter(
        order__order_number=order_number)
    context = {
        'order_products': order_products,
        'order': order,
    }
    return render(request, 'dashboard/order_details.html', context)


def users(request):
    users = User.objects.all()
    context = {
        'users': users
    }
    return render(request, 'dashboard/users.html', context)


def user_status(request, user_id):
    user = User.objects.get(id=user_id)
    if user.is_active:
        user.is_active = False
        user.save()
        return redirect('users')
    else:
        user.is_active = True
        user.save()
        return redirect('users')


def categories(request):
    categories = Book_Category.objects.annotate(
        total_books=Count('books'))

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('categories')
    else:

        form = CategoryForm()

    return render(request, 'dashboard/categories.html', {'form': form, 'categories': categories})


def delete_category(request, cat_id):
    category = Book_Category.objects.get(id=cat_id)
    category.delete()
    return redirect('categories')


def edit_category(request, cat_id):
    categories = Book_Category.objects.annotate(
        total_books=Count('books'))
    category = Book_Category.objects.get(id=cat_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
        return redirect('categories')

    else:
        form = CategoryForm(instance=category)
    return render(request, 'dashboard/categories.html', {'form': form, 'categories': categories})


def coupons(request):
    coupons = Coupon.objects.all()
    context = {
        'coupons': coupons
    }
    return render(request, 'dashboard/coupons.html', context)


def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('coupons')

    else:
        form = CouponForm()
    context = {'form': form}

    return render(request, 'dashboard/add_coupon.html', context)


def delete_coupon(request, coupon_id):
    coupon = Coupon.objects.get(id=coupon_id)
    coupon.delete()
    return redirect('coupons')


def change_status(request, order_number):
    if request.method == 'POST':
        status = request.POST.get('status')
        order = Order.objects.get(order_number=order_number)
        if order.status != status:
            order.status = status
        else:
            return redirect('orders')

        order.save()
        return redirect('orders')


def search_order(request):
    status_choices = Order.STATUS
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            orders = Order.objects.filter(
                Q(order_number__icontains=keyword) | Q(first_name__icontains=keyword))

    context = {
        'orders': orders,
        'status_choices': status_choices
    }
    return render(request, 'dashboard/orders.html', context)


def sales_report(request):

    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        if start_date and end_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            sales_data = Order.objects.filter(
                created_at__gte=start_date, created_at__lte=end_date)
        else:
            sales_data = Order.objects.all()

        context = {
            'data': sales_data,
            'start_date': start_date,
            'end_date': end_date
        }
        template_path = 'dashboard/sales_report.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="sales_report_{start_date}.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            messages.error(request, 'Report Generating failed')
        return response
    else:
        return redirect('orders')
