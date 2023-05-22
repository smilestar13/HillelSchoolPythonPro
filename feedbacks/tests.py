import pytest
from django.urls import reverse


def test_url(client):
    url = reverse('feedbacks')
    response = client.get(url)
    assert response.status_code == 200
