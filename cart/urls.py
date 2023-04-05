from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:book_id>', views.add_cart, name='add_cart'),
    path('remove_cart/<int:book_id>', views.remove_cart, name='remove_cart'),
    path('delete_cart_item/<int:book_id>',
         views.delete_cart_items, name='delete_cart_item')

]
