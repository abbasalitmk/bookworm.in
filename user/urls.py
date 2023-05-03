from django.urls import path
from . import views
from cart.views import add_to_wishlist, move_to_cart
from django.utils.text import slugify


urlpatterns = [
    path('', views.home, name='home'),
    path('my_account/', views.my_account, name='my_account'),
    path('my_account/address', views.view_addresses, name='view_addresses'),
    path('my_account/address/add', views.create_address, name='create_address'),
    path('my_account/address/edit/<int:address_id>',
         views.edit_address, name='edit_address'),

    path('my_account/address/delete/<int:address_id>',
         views.delete_address, name='delete_address'),
    path('my_account/orders', views.my_account, name='my_orders'),
    path('my_account/wishlist', views.wishlist, name='wishlist'),
    path('my_account/wishlist/add/<int:books_id>',
         add_to_wishlist, name='add_to_wishlist'),
    path('my_account/wishlist/move/<int:book_id>',
         move_to_cart, name='move_to_cart'),

    path('profile/change_password/<int:id>',
         views.changePassword, name='new_password'),

    path('books/', views.list_book, name='books'),

    path('books/category=<str:cat_name>',
         views.category_list, name='category_list'),

    path('books/filter_price',
         views.filter_price, name='filter_price'),
    path('books/detail/<str:title>', views.book_details, name='book-details'),
    path('search', views.searchBook, name='search'),
    path('book_review/<int:book_id>', views.book_review, name='book_review'),
    path('password_change/', views.password_change_view, name='password_change'),







]
