from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add_cart/<int:book_id>', views.add_cart, name='add_cart'),
    path('increment_cart_item/<int:cart_item_id>/',
         views.increment_cart_item, name='increment_cart_item'),
    path('decrement_cart_item/<int:cart_item_id>/',
         views.decrement_cart_item, name='decrement_cart_item'),
    path('delete_Cart/<int:cart_item_id>/',
         views.delete_Cart, name='delete_Cart'),
    path('checkout', views.checkout, name='checkout'),
    path('apply_coupon', views.apply_coupon, name='coupon'),
    path('order_summary', views.order_summary, name='order_summary'),
    path('remove_from_wishlist/<int:book_id>', views.remove_from_wishlist,
         name='remove_from_wishlist')

]
