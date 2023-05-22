import pytest
from django.urls import reverse

def test_cart(client):
    url = reverse('order')
    response = client.get(url, follow=True)
    assert response.status_code == 200
    assert '/en' + response.redirect_chain[0][0] == reverse('login') + f'?next={url}'
    assert response.redirect_chain[0][1] == 302