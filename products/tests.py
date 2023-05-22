import pytest
from django.urls import reverse

from currencies.models import CurrencyHistory
from products.models import Product, Category
from project.constants import DECIMAL_PLACES, MAX_DIGITS


def test_product_list(client, faker):
    CurrencyHistory.objects.create(
        code='USD',
        bank_name='TestBank'
    )
    for _ in range(10):
        Product.objects.create(
            name=faker.word(),
            sku=faker.word(),
            price=faker.pydecimal(
                min_value=0,
                left_digits=DECIMAL_PLACES,
                right_digits=MAX_DIGITS - DECIMAL_PLACES
            )
        )
    url = reverse('products')
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.context['products']) == Product.objects.count()
