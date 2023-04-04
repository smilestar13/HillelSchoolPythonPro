from django import forms
from django.core.exceptions import ValidationError

from products.models import Product

class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'sku', 'image', 'price')

    def clean_name(self):
        try:
            Product.objects.get(name=self.cleaned_data['name'])
            raise ValidationError('Product already exist.')
        except Product.DoesNotExist:
            ...
        return self.cleaned_data['name']
