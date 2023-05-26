import pytest
from django.urls import reverse

from currencies.models import CurrencyHistory
from products.models import Product
from project.constants import DECIMAL_PLACES, MAX_DIGITS

from io import StringIO
import decimal
import csv
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from products.forms import ImportCSVForm


def test_product_list(client, faker, product_factory):
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

    product = product_factory()
    response = client.get(reverse('product', kwargs={'pk': product.pk}))
    assert response.status_code == 200


def test_import_csv_form_clean_file():
    form = ImportCSVForm()
    csv_data = StringIO()
    csv_writer = csv.DictWriter(csv_data, fieldnames=['name', 'description', 'price', 'sku', 'is_active'])
    csv_writer.writeheader()
    csv_writer.writerow({'name': 'Test Product', 'description': 'Test Description', 'price': '9.99',
                         'sku': 'TEST-SKU', 'is_active': 'True'})
    csv_file = SimpleUploadedFile('test.csv', csv_data.getvalue().encode('utf-8'))

    form.cleaned_data = {'file': csv_file}
    products_list = form.clean_file()
    assert len(products_list) == 1

    product = products_list[0]
    assert product.name == 'Test Product'
    assert product.description == 'Test Description'
    assert product.price == decimal.Decimal('9.99')
    assert product.sku == 'TEST-SKU'
    assert product.is_active == 'True'

    csv_data_invalid = StringIO()
    csv_writer_invalid = csv.DictWriter(csv_data_invalid, fieldnames=['name', 'description', 'price'])
    csv_writer_invalid.writeheader()
    csv_writer_invalid.writerow({'name': 'Test Product', 'description': 'Test Description', 'price': 'invalid'})
    csv_file_invalid = SimpleUploadedFile('test_invalid.csv', csv_data_invalid.getvalue().encode('utf-8'))
    form.cleaned_data = {'file': csv_file_invalid}
    with pytest.raises(ValidationError):
        form.clean_file()