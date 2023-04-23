from django.db import models
from dashboard.models import Book, Variation
from accounts.models import CustomUser as User


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variation, blank=True)

    def sub_total(self):
        return self.book.price * self.quantity

    def __unicode__(self):
        return self.book


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ManyToManyField(Book)

    def __str__(self):
        return self.user.first_name + 'Wishlist'
