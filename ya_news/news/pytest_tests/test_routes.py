from http import HTTPStatus

from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    'name_url, args',
    (
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('id_news')),
    ),
)
def test_page_availability_for_anonymous_user(args, client, name_url):
    url = reverse(name_url, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'user_client, expected_status',
    (
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
        (pytest.lazy_fixture('reader_client'), HTTPStatus.NOT_FOUND),
    ),
)
@pytest.mark.parametrize(
    'name_url, args',
    (
        ('news:edit', pytest.lazy_fixture('id_comment')),
        ('news:delete', pytest.lazy_fixture('id_comment')),
    ),
)
def test_availability_comment_edit_and_delete(
    args, name_url, user_client, expected_status
):
    url = reverse(name_url, args=args)
    response = user_client.get(url)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'name_url, args',
    (
        ('news:edit', pytest.lazy_fixture('id_comment')),
        ('news:delete', pytest.lazy_fixture('id_comment')),
    ),
)
def test_redirect_edit_delete_for_anonymous(args, name_url, client):
    login_url = reverse('users:login')
    url = reverse(name_url, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
