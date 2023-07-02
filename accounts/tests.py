import pytest

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.cache import cache

from accounts.models import UserManager

User = get_user_model()


def test_login(client, faker):
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())
    data['username'] = faker.email()
    data['password'] = faker.word()

    response = client.post(url, data=data)
    assert response.status_code == 200
    assert response.context['form'].errors['__all__'] == [
        'Please enter a correct email address and password. Note that both fields may be case-sensitive.']

    password = faker.word()
    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    user.set_password(password)
    user.save()

    data['username'] = user.email
    data['password'] = password

    response = client.post(url, data=data)
    assert response.status_code == 302


def test_registration(client, faker):
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200

    data = {}
    response = client.post(url, data=data)
    assert response.status_code == 200
    assert all(v == ['This field is required.']
               for v in response.context['form'].errors.values())

    user, _ = User.objects.get_or_create(
        email=faker.email(),
    )
    password = faker.word()
    data = {
        'email': user.email,
        'password1': password,
        'password2': faker.word()
    }
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['email'] == ['User already exist.']
    assert errors['password2'] == ['The two password fields didn’t match.']

    data['email'] = faker.email()
    data['password2'] = password
    response = client.post(url, data=data)
    assert response.status_code == 200
    errors = response.context['form'].errors
    assert errors['password2'] == [
        'This password is too short. It must contain at least 8 characters.']

    password = faker.password()
    data['password1'] = password
    data['password2'] = password
    response = client.post(url, data=data, follow=True)
    assert response.status_code == 200
    assert response.redirect_chain[0][0] == reverse('main')
    assert response.redirect_chain[0][1] == 302


def test_update_phone_view_get(login_client, client):
    client, user = login_client()
    url = reverse('update_phone')
    response = client.get(url)

    assert response.status_code == 200

    url = reverse('update_phone')
    confirmation_code = 'ABCD123'
    cache.set('confirmation_code', confirmation_code, 60)

    data = {
        'phone': '1234567890',
        'code': 'INVALID'
    }
    response = client.post(url, data=data)

    assert response.status_code == 200


def test_profile(login_client, client):
    client, user = login_client()
    url = reverse('profile')
    response = client.get(url)

    assert response.status_code == 200


def test_user_manager_create_superuser():
    email = 'admin@example.com'
    password = 'admin123'
    user = User.objects.create_superuser(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)
    assert user.is_staff
    assert user.is_superuser

    email = 'user@example.com'
    password = 'user123'
    extra_fields = {
        'is_staff': True,
        'is_superuser': False,
    }
    user = User.objects.create_user(email=email, password=password, **extra_fields)

    assert user.email == email
    assert user.check_password(password)
    assert user.is_staff == extra_fields['is_staff']
    assert user.is_superuser == extra_fields['is_superuser']




