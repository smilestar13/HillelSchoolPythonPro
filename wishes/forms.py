from django import forms
from django.core.exceptions import ValidationError

from orders.models import Discount
from products.models import Product
from wishes.models import WishListItem


class WishesForm(forms.Form):
    discount = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        self.fields.update({k: forms.IntegerField() if k.startswith(
            'quantity') else forms.UUIDField() for k in self.data.keys() if
                            k.startswith(('quantity', 'item'))})

    def clean_discount(self):
        if self.cleaned_data['discount']:
            try:
                discount = Discount.objects.get(
                    code=self.cleaned_data['discount']
                )
                if not discount.is_valid:
                    raise ValidationError
            except (Discount.DoesNotExist, ValidationError):
                raise ValidationError('Invalid discount code.')
            return discount

    def save(self):
        for k in self.cleaned_data.keys():
            if k.startswith('item_'):
                index = k.split('_')[-1]
                try:
                    item = WishListItem.objects.select_for_update().get(
                        id=self.cleaned_data[f'item_{index}']
                    )
                except WishListItem.DoesNotExist:
                    raise ValidationError('Something wrong!')
                item.quantity = self.cleaned_data[f'quantity_{index}']
                item.save(update_fields=('quantity',))
        discount = self.cleaned_data.get('discount')
        if discount:
            self.instance.discount = discount
            self.instance.save(update_fields=('discount',))
        return self.instance


class WishActionForm(forms.Form):
    product_id = forms.UUIDField(required=False)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    def clean_product_id(self):
        if self.cleaned_data['product_id']:
            try:
                return Product.objects.get(id=self.cleaned_data['product_id'])
            except Product.DoesNotExist:
                raise ValidationError('Wrong product id.')

    def action(self, action):
        if action == 'add':
            product = self.cleaned_data['product_id']
            WishListItem.objects.get_or_create(
                wish_list=self.instance,
                product=product,
                defaults=dict(price=product.price)
            )

        if action == 'pay':
            self.instance.is_active = False
            self.instance.is_paid = True
            self.instance.save(update_fields=('is_active', 'is_paid'))

        if action == 'remove':
            product = self.cleaned_data['product_id']
            WishListItem.objects.filter(wish_list=self.instance,
                                        product=product).delete()

        if action == 'clear':
            WishListItem.objects.filter(wish_list=self.instance).delete()
