from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard'),
    path('books=grid', views.product_grid, name='books_grid'),
    path('books=list', views.product_list, name='books_list'),

    path('book/add', views.add_book, name='add_book'),
    path('orders', views.orders, name='orders'),
    path('payment', views.payment, name='payment'),
    path('book/edit/<int:book_id>', views.edit_book, name='edit_book'),
    path('book/delete/<int:book_id>', views.delete_book, name='delete_book'),
    path('orders/details/<int:order_number>',
         views.order_details, name='order_details'),
    path('users', views.users, name='users'),
    path('users/status/<int:user_id>', views.user_status, name='user_status'),
    path('book/category', views.categories, name='categories'),
    path('book/category/delete/<int:cat_id>',
         views.delete_category, name='delete_category'),
    path('book/search',
         views.search_books, name='search_books'),

    path('book/category/edit/<int:cat_id>',
         views.edit_category, name='edit_category'),
    path('coupons',
         views.coupons, name='coupons'),
    path('coupons/add',
         views.add_coupon, name='add_coupon'),
    path('coupons/delete/<int:coupon_id>',
         views.delete_coupon, name='delete_coupon'),
    path('orders/status/<int:order_number>',
         views.change_status, name='change_status'),
    path('orders/search',
         views.search_order, name='search_order'),
    path('report',
         views.sales_report, name='report'),









]
