from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('profile/', views.profile, name='profile'),

    path('profile/change_password/<int:id>',
         views.changePassword, name='new_password'),

    path('books/', views.list_book, name='books'),

    path('books/category=<str:cat_name>',
         views.category_list, name='category_list'),

    path('books/category/<str:cat_name>/<int:min_price>-<int:max_price>',
         views.category_list, name='price_list'),
    path('books/detail/<str:title>', views.book_details, name='book-details'),
    path('search', views.searchBook, name='search')






]
