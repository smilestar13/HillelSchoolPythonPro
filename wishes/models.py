import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Sum, F
from django_lifecycle import hook, AFTER_UPDATE, LifecycleModelMixin, \
    AFTER_SAVE

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from project.model_choices import DiscountTypes
from orders.models import Discount

User = get_user_model()


class WishList(LifecycleModelMixin, PKMixin):
    total_amount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    discount = models.ForeignKey(
        Discount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    is_active = models.BooleanField(default=True)
    is_paid = models.BooleanField(default=False)
    wishlist_number = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user'],
                                    condition=models.Q(is_active=True),
                                    name='wishes_unique_is_active')
        ]

    def __str__(self):
        return f"{self.user} | {self.total_amount}"

    @property
    def is_current_order(self):
        return self.is_active and not self.is_paid

    def get_total_amount(self):
        total_amount = self.wish_list_items.aggregate(
            total_amount=Sum(F('price') * F('quantity'))
        )['total_amount'] or 0

        if self.discount and self.discount.is_valid:
            total_amount = (
                total_amount - self.discount.amount
                if self.discount.discount_type == DiscountTypes.VALUE else
                total_amount - (total_amount / 100 * self.discount.amount)
            ).quantize(decimal.Decimal('.01'))
        return total_amount

    @hook(AFTER_UPDATE, when='discount', has_changed=True)
    def set_total_amount(self):
        self.total_amount = self.get_total_amount()
        self.save(update_fields=('total_amount',), skip_hooks=True)


class WishListItem(LifecycleModelMixin, PKMixin):
    wish_list = models.ForeignKey(
        WishList,
        on_delete=models.CASCADE,
        related_name='wish_list_items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.PROTECT,
        related_name='wish_list_items',
    )
    quantity = models.PositiveSmallIntegerField(default=1)
    price = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES
    )

    class Meta:
        unique_together = ('wish_list', 'product')

    @property
    def sub_total(self):
        return self.price * self.quantity

    @hook(AFTER_SAVE)
    def set_order_total_amount(self):
        self.wish_list.total_amount = self.wish_list.get_total_amount()
        self.wish_list.save(update_fields=('total_amount',), skip_hooks=True)
