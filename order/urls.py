from django.urls import path
from . import views


urlpatterns = [

    path('place_order', views.place_order, name='place_order'),

    path('payment_handler', views.payment, name='payment_handler'),
    path('order_confirmed', views.order_confirmed, name='order_confirmed'),
    path('verify_payment', views.payment, name='verify_payment'),
    path('cash_on_delivery/<int:order_number>',
         views.cash_on_delivery, name='cash_on_delivery'),
    path('cancel_order/<int:order_number>',
         views.cancel_order, name='cancel_order'),
    path('generate_invoice/<int:order_number>',
         views.generate_invoice, name='generate_invoice')



]
