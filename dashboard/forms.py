from django import forms
from .models import Book, Book_Category, BookVariation, Author, Image, Coupon
from django.forms import DateInput
from .models import Review


class BookForm(forms.ModelForm):
    # categories = forms.ModelMultipleChoiceField(
    #     queryset=Book_Category.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    variation_type = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control mb-3'}), required=False)
    variation_price = forms.DecimalField(widget=forms.NumberInput(
        attrs={'class': 'form-control'}), required=False)
    author_name = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    image = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'onchange': 'previewImage1(event)'}))
    image2 = forms.ImageField(widget=forms.FileInput(
        attrs={'class': 'form-control', 'onchange': 'previewImage2(event)'}), required=False)

    class Meta:
        model = Book
        fields = [
            'title', 'price', 'discount', 'publishing_date', 'description', 'book_type',
            'language', 'stock', 'categories'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'discount': forms.TextInput(attrs={'class': 'form-control'}),
            'publishing_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'height:15vh'}),
            'book_type': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.TextInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'categories': forms.CheckboxSelectMultiple(),


        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.fields['categories'].queryset = Book_Category.objects.all()
            self.fields['categories'].initial = instance.categories.all()


class CategoryForm(forms.ModelForm):

    class Meta:

        model = Book_Category
        fields = [
            'name'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CouponForm(forms.ModelForm):

    class Meta:
        model = Coupon
        fields = ['coupon_text', 'discount_percentage', 'discount_amount']

        widgets = {
            'discount_percentage': forms.NumberInput(attrs={'min': 0, 'max': 100}),
            'discount_amount': forms.NumberInput(attrs={'min': 0}),
        }


class GetYear(forms.Form):
    start_date = forms.DateField(input_formats=['%Y'], widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'class': 'form-control', }))
    end_date = forms.DateField(input_formats=['%Y'], widget=forms.widgets.DateInput(
        attrs={'type': 'date', 'class': 'form-control', }))


class Review_form(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'review_text']
