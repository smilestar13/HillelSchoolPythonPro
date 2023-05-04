from os import path

from django.db import models
from django.core.validators import MinValueValidator

from project.constants import MAX_DIGITS, DECIMAL_PLACES
from project.mixins.models import PKMixin
from django.utils.safestring import mark_safe

from project.model_choices import Currencies


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class Category(PKMixin):
    name = models.CharField(max_length=128)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="max-height: 100px;" />' % self.image.url) # noqa
        else:
            return '(No image)'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f"{self.name.title()} | {self.description.title()}"

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Product(PKMixin):
    name = models.CharField(max_length=255)
    description = models.TextField(
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to=upload_to, null=True, blank=True)
    sku = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES)
    categories = models.ManyToManyField(Category, blank=True)
    products = models.ManyToManyField("products.Product", blank=True)
    currency = models.CharField(
        max_length=16,
        choices=Currencies.choices,
        default=Currencies.UAH
    )
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="max-height: 100px;" />' % self.image.url) # noqa
        else:
            return '(No image)'

    image_tag.short_description = 'Image'

    def __str__(self):
        return f"Name = {self.name.title()} | Price = {self.price} UAH"
