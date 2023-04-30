from django.db import models
from accounts.models import CustomUser as User
from dashboard.models import Book
from cart.models import BookVariation


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.payment_id


class Order(models.Model):

    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled')
    )
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True)
    order_number = models.CharField(max_length=100)

    status = models.CharField(max_length=50, default='New', choices=STATUS)
    ip = models.CharField(max_length=50, blank=True)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address_line1 = models.CharField(max_length=100)
    address_line2 = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50, blank=True)
    state = models.CharField(max_length=50, blank=True)
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    provider_order_id = models.CharField(max_length=50, blank=True, null=True)

    def fullname(self):
        return self.first_name + ' ' + self.last_name


class OrderProduct(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='order_product')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    variation = models.ManyToManyField(BookVariation, blank=True)
    quantity = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Razorpay(models.Model):
    order_id = models.CharField(max_length=150)
    payment_id = models.CharField(max_length=150, null=True)
    signature_id = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=200, default='pending')
    payment_id = models.CharField(max_length=200, null=True)
