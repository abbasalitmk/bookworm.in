from django.contrib import admin
from .models import Book, Image, Category, Author


class ImageInline(admin.TabularInline):
    model = Image


class AuthorInline(admin.TabularInline):
    model = Author


class CategoryInline(admin.TabularInline):
    model = Category


class BookAdmin(admin.ModelAdmin):
    inlines = [ImageInline, AuthorInline, CategoryInline]


admin.site.register(Book, BookAdmin)
