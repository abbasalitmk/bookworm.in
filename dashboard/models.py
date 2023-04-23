from django.db import models
from django.utils.text import slugify


class Book_Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    publishing_date = models.DateField()
    description = models.TextField()
    book_type = models.CharField(max_length=100)
    language = models.CharField(max_length=60)
    stock = models.IntegerField()
    categories = models.ManyToManyField(Book_Category, related_name='books')

    def __str__(self):
        return self.title


class Image(models.Model):
    url = models.ImageField(upload_to='book_covers/')
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='image')


class Author(models.Model):
    name = models.CharField(max_length=200)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='author')


variation_category_choices = (
    ('Type', 'Type'),
    ('Edition', 'Edition')
)


class VariationManager(models.Manager):

    def edition(self):
        return super(VariationManager, self).filter(variation_category='Edition', is_active=True)

    def book_type(self):
        return super(VariationManager, self).filter(variation_category='Type', is_active=True)


class Variation(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(
        max_length=100, choices=variation_category_choices)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now=True)

    objects = VariationManager()

    def __str__(self):
        return self.variation_value


class Coupon (models.Model):
    coupon_text = models.CharField(max_length=150, unique=True)
    discount_percentage = models.IntegerField(blank=True, null=True)
    discount_amount = models.IntegerField()


class BookVariation(models.Model):
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='book_variation', blank=True)
    variation_type = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return f"{self.book.title} ({self.variation_type})"
