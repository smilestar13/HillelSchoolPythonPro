from django.urls import reverse

from currencies.models import CurrencyHistory


def test_wishes(client, login_client, product_factory, faker):
    url = reverse('favourites')
    response = client.get(url, follow=True)
    CurrencyHistory.objects.create(
        code='USD',
        bank_name='TestBank'
    )
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302

    client, user = login_client()
    response = client.get(url)
    assert response.status_code == 200
    assert not response.context['wish_items']
    wish_list = response.context['wish']
    assert wish_list
    assert not wish_list.wish_list_items.exists()
    #
    product = product_factory()
    data = {
        'product_id': faker.uuid4()
    }
    response = client.post(reverse('wish_list_action', args=('add',)), data=data,
                           follow=True)
    assert response.status_code == 200
    assert not wish_list.wish_list_items.exists()

    data['product_id'] = str(product.id)
    response = client.post(reverse('wish_list_action', args=('add',)), data=data,
                           follow=True)
    assert response.status_code == 200
    wish_list_item = wish_list.wish_list_items.first()
    assert wish_list_item.product == product
    assert wish_list_item.quantity == 1
    assert wish_list_item.price == product.price

    data = {
        'item_1': str(wish_list_item.id),
        'quantity_1': 5
    }
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    wish_list_item.refresh_from_db()
    assert wish_list_item.quantity == data['quantity_1']

    client.post(reverse('wish_list_action', args=('clear',)), data={}, follow=True)
    assert not wish_list.wish_list_items.exists()

    data['product_id'] = str(product.id)
    response = client.post(reverse('wish_list_action', args=('add',)), data=data,
                           follow=True)
    assert response.status_code == 200
    wish_list_item = wish_list.wish_list_items.first()
    assert wish_list_item.product == product
    client.post(reverse('wish_list_action', args=('remove',)), data=data, follow=True)

    data['product_id'] = str(product.id)
    response = client.post(reverse('wish_list_action', args=('add',)), data=data,
                           follow=True)
    assert response.status_code == 200
    wish_list_item = wish_list.wish_list_items.first()
    assert wish_list_item.product == product
    client.post(reverse('wish_list_action', args=('pay',)), data=data, follow=True)