from dashboard.models import Book_Category, Book
from django.db.models import Count


def category_slugs(request):
    category_links = Book_Category.objects.annotate(count_book=Count('books'))

    return dict(category_links=category_links)
