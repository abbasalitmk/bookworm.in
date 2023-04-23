from django.urls import path
from . import views
from cart.views import add_to_wishlist, move_to_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('my_account/', views.my_account, name='my_account'),
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
    path('search', views.searchBook, name='search')







]
