from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2)
    publishing_date = models.DateField()
    description = models.TextField()
    book_type = models.CharField(max_length=100)
    language = models.CharField(max_length=60)

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


class Category(models.Model):
    CATEGORIES = [
        ('fiction', 'fiction'),
        ('novel', 'novel'),
        ('biography', 'biography'),
        ('story', 'story'),
        ('history', 'history')
    ]
    cat_name = models.CharField(max_length=100, choices=CATEGORIES)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name='category')
