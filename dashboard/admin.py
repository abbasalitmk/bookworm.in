from django.contrib import admin
from .models import Book, Image, Author, Variation, Coupon, Book_Category, BookVariation, Review


class ImageInline(admin.TabularInline):
    model = Image


class AuthorInline(admin.TabularInline):
    model = Author


class BookAdmin(admin.ModelAdmin):
    inlines = [ImageInline, AuthorInline]


class VariationAdmin(admin.ModelAdmin):
    list_display = ('book', 'variation_category',
                    'variation_value', 'is_active')
    list_editable = ('is_active'),


admin.site.register(Book)
admin.site.register(Book_Category)
admin.site.register(Variation)
admin.site.register(BookVariation)
admin.site.register(Image)
admin.site.register(Coupon)
admin.site.register(Review)
