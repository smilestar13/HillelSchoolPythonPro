import pytest
from django.urls import reverse

from feedbacks.forms import FeedbackModelForm
from feedbacks.models import Feedback


def test_url(client):
    url = reverse('feedbacks')
    response = client.get(url)
    assert response.status_code == 200


def test_feedback_model_form_clean_method(login_client, client):
    client, user = login_client()

    form = FeedbackModelForm(user=user, data={
        'text': 'Test feedback',
        'rating': 5
    })
    assert form.fields['rating'].help_text == "Rating should be from 1 to 5 💫"

def test_feedbacks_view(client, login_client):
    client, user = login_client()
    url = reverse('feedback_create')
    response = client.post(url, data={
        'text': 'Test feedback',
        'rating': 5
    })
    assert response.status_code == 200

