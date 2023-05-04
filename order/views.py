import hmac
from django.http import HttpResponseBadRequest, HttpResponse
import json
import hashlib
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from cart.models import CartItem
from user.models import Address
from .models import Order, Payment, Razorpay, OrderProduct
from dashboard.models import Book, Coupon
from .forms import OrderForm
import datetime
import razorpay
from django.conf import settings
from decimal import Decimal
import math
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.template.loader import render_to_string


def order_now(request):
    if request.method == 'POST':
        address = request.POST['address']
        payment_method = request.POST['payment_method']

    return HttpResponse(address)


@ login_required(login_url='login')
def place_order(request, total=0, quantity=0, cart_items=None, delivery_charge=0, sub_total=0):

    context = {}
    variation_price = 0
    paperback_price = 0

    current_user = request.user
    cart_item = CartItem.objects.filter(user=current_user)

    for item in cart_item:
        if item.variation:
            try:
                variation = item.variation.get()
                price = variation.price
                variation_price += (price * item.quantity)
            # variation_price = item.variation.price
            # cart_total += (book_price * item.quantity)
            except:

                paperback_price += (item.book.price * item.quantity)
            quantity += item.quantity

        total = variation_price + paperback_price

    if total < 500:
        delivery_charge = 45
    else:
        delivery_charge = 0

    gst = (total * 5)/100
    grand_total = math.ceil(total+gst+delivery_charge)

    cart_count = cart_item.count()

    if cart_count <= 0:
        return redirect('checkout')

    order_number = ''

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')

        current_user = request.user
        address_value = request.POST.get('address')
        if address_value is None:
            messages.warning(request, 'Please select address')
            return redirect('checkout')
        address = Address.objects.get(id=address_value)

        order = Order()
        order.user = current_user
        order.first_name = address.first_name
        order.last_name = address.last_name
        order.phone = address.phone
        order.email = address.email
        order.address_line1 = address.address_line1
        order.address_line2 = address.address_line2
        order.pincode = address.pincode
        order.city = address.city
        order.country = address.country
        order.state = address.state
        order.tax = gst
        order.ip = '127.1.1.0'
        order.save()

        # generate order number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        m = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, m, dt)
        current_date = d.strftime("%Y%m%d")
        order_number = current_date + str(order.id)

        order.order_number = order_number
        order.save()

        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line1 = form.cleaned_data['address_line1']
            data.address_line2 = form.cleaned_data['address_line2']
            data.pincode = form.cleaned_data['pincode']
            data.city = form.cleaned_data['city']
            data.country = form.cleaned_data['country']
            data.state = form.cleaned_data['state']
            data.tax = gst
            data.ip = '127.1.1.0'
            data.save()

        coupon_discount = request.session.get('discount')
        if coupon_discount:
            grand_total = grand_total-coupon_discount

        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

        razor_order = client.order.create({
            'amount': grand_total*100,
            'currency': 'INR',
            'payment_capture': '1',  # auto-capture payment
        })

        if razor_order['status'] != 'created':
            messages.error(
                request, 'Error processing payment. Please try again later.')
            return redirect('checkout')

        order.provider_order_id = razor_order['id']
        order.order_total = razor_order['amount']/100

        order.save()

        context = {
            'order_item': Order.objects.filter(user=current_user, is_ordered=False, order_number=order_number),
            'cart_item': cart_item,
            'total': total,
            'quantity': quantity,
            'delivery_charge': delivery_charge,
            'gst': gst,
            'grand_total': grand_total,
            'sub_total': sub_total,
            'razorpay_order_id': razor_order['id'],
            'razorpay_amount': razor_order['amount'],
            'razorpay_currency': razor_order['currency'],
            'razorpay_key_id': settings.RAZOR_KEY_ID,
            'coupon_discount': coupon_discount,
            'order_number': order_number

        }

    return render(request, 'place_order.html', context)


@csrf_exempt
def payment(request):
    if request.method == 'POST':
        razorpay_payment_id = request.POST['razorpay_payment_id']
        razorpay_order_id = request.POST['razorpay_order_id']
        razorpay_signature = request.POST['razorpay_signature']
        # Verify Signature
        signature = hmac.new(bytes(settings.RAZOR_KEY_SECRET, 'utf-8'), msg=bytes(
            f"{razorpay_order_id}|{razorpay_payment_id}", 'utf-8'), digestmod=hashlib.sha256)
        generated_signature = signature.hexdigest()
        if generated_signature != razorpay_signature:
            messages.error(request, 'Invalid Payment Request')
        # Verify Payment
        client = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        razor_payment = client.payment.fetch(razorpay_payment_id)
        if razor_payment['status'] != 'captured':
            messages.error(request, 'Payment Not Captured')
            return redirect('checkout')
        else:
            # Update payment status and create payment object
            order = Order.objects.get(
                provider_order_id=request.POST['razorpay_order_id'])
            amount = round(order.order_total)
            payment_model = Payment.objects.create(
                user=request.user,
                payment_id=request.POST['razorpay_payment_id'],
                payment_method='Razorpay',
                amount_paid=amount,
                status='Success'
            )
            # Update order status and create order object
            order.status = 'Accepted'
            order.payment = payment_model
            order.is_ordered = True
            order.order_total = amount
            order.save()
            # Create order product object(s)
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                order_product = OrderProduct.objects.create(
                    order=order,
                    user=request.user,
                    payment=payment_model,
                    book=item.book,
                    quantity=item.quantity,
                )
                order_product.save()
                # set the variations for this OrderProduct
                order_product.variation.set(item.variation.all())
                order_product.save()
                # Decrease book quantity
            book = Book.objects.get(id=item.book_id)
            book.stock -= item.quantity
            book.save()
            # Clear cart
            CartItem.objects.filter(user=request.user).delete()
            context = {
                'products': OrderProduct.objects.filter(order=order)
            }

            # send email to user when order confirmed
            subject = 'Order Confirmation'
            message = 'Thank you for your order. Your order has been confirmed.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [order.email]

            context = {
                'customer_name': order.first_name,

            }
            html_message = render_to_string('email_template.html', context)

            send_mail(subject, '', email_from,
                      recipient_list, fail_silently=False, html_message=html_message,)

            return redirect('order_confirmed')
    else:
        return HttpResponse("invalid payment method")


@csrf_exempt
def order_confirmed(request):

    return render(request, 'order_success.html')


@ login_required(login_url='login')
def cash_on_delivery(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)

        amount = round(order.order_total)

        payment_model = Payment.objects.create(
            user=request.user,
            payment_id=order_number,
            payment_method='COD',
            amount_paid=amount,
            status='Success'
        )

        # Update order status and create order object

        order.status = 'Accepted'
        order.payment = payment_model
        order.is_ordered = True
        order.order_total = amount + order.tax
        order.save()

        # Create order product object(s)
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                user=request.user,
                payment=payment_model,
                book=item.book,
                quantity=item.quantity,
            )

            order_product.save()
            # set the variations for this OrderProduct
            order_product.variation.set(item.variation.all())
            order_product.save()

        # Decrease book quantity
        book = Book.objects.get(id=item.book_id)
        book.stock -= item.quantity
        book.save()

        # Clear cart
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, 'Order placed successfully')

        # send mail to uer when order complete
        subject = 'Order Confirmation'
        message = 'Thank you for your order. Your order has been confirmed.'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [order.email]

        context = {
            'customer_name': order.first_name,

        }
        html_message = render_to_string('email_template.html', context)

        send_mail(subject, '', email_from,
                  recipient_list, fail_silently=False, html_message=html_message,)

        return redirect('order_confirmed')
    except:
        messages.error(request, 'Error, Invlaid Payment')
        return redirect('checkout')


@ login_required(login_url='login')
def cancel_order(request, order_number):
    order = Order.objects.get(order_number=order_number)
    payment_model = Payment.objects.get(order=order)
    if order.payment.status == 'Success':
        if payment_model.payment_method == 'COD':
            order.status = 'Cancelled'
            order.save()
            payment_model.status = 'Cancelled'
            payment_model.save()

        else:

            # Initialize the Razorpay client with your API keys
            razorpay_client = razorpay.Client(
                auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

            # Retrieve the payment ID and amount from your Django order object
            payment_id = order.payment.payment_id
            # amount in paise (e.g. Rs. 10.00 = 1000 paise)
            amount = Decimal(order.payment.amount_paid)*100

            # Check if the payment has been captured and is refundable
            payment = razorpay_client.payment.fetch(payment_id)
            if payment['status'] != 'captured':
                messages.error(request, 'Payment cannot be refunded')

            else:

                # Create a refund object using the Razorpay API
                refund_data = {
                    'payment_id': payment_id,
                    'amount': str(amount),
                    'notes': {'reason': 'User cancelled order'}
                }
                refund = razorpay_client.refund.create(data=refund_data)

                # Update the status of the order in your Django application
                order.status = 'Cancelled'

                payment_model.status = 'REFUND_INITIATED'
                order.save()
                payment_model.save()
                # Monitor the status of the refund using the Razorpay API
                refund = razorpay_client.refund.fetch(refund['id'])

                # If the refund is successful, update the status of the order in your Django application
                if refund['status'] == 'processed':
                    payment_model.status = 'REFUNDED'
                    payment_model.save()

        return redirect('my_orders')


@ login_required(login_url='login')
def generate_invoice(request, order_number):
    order = Order.objects.get(order_number=order_number)

    if request.method == 'GET':

        context = {
            'data': order,

        }
        template_path = 'invoice.html'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="invoice_{order_number}.pdf"'

        template = get_template(template_path)
        html = template.render(context)
        pisa_status = pisa.CreatePDF(html, dest=response)

        if pisa_status.err:
            messages.error(request, 'Report Generating failed')
        return response
    else:
        return redirect('my-orders')
