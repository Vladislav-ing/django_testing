from http.client import NOT_FOUND, OK

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url, user_client, status_code',
    (
        (
            pytest.lazy_fixture('login_url'),
            pytest.lazy_fixture('client'),
            OK,
        ),
        (
            pytest.lazy_fixture('login_url'),
            pytest.lazy_fixture('reader_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('logout_url'),
            pytest.lazy_fixture('client'),
            OK,
        ),
        (
            pytest.lazy_fixture('logout_url'),
            pytest.lazy_fixture('reader_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('signup_url'),
            pytest.lazy_fixture('client'),
            OK,
        ),
        (
            pytest.lazy_fixture('signup_url'),
            pytest.lazy_fixture('reader_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('home_url'),
            pytest.lazy_fixture('client'),
            OK,
        ),
        (
            pytest.lazy_fixture('home_url'),
            pytest.lazy_fixture('reader_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('detail_url'),
            pytest.lazy_fixture('client'),
            OK,
        ),
        (
            pytest.lazy_fixture('detail_url'),
            pytest.lazy_fixture('reader_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('edit_comment_url'),
            pytest.lazy_fixture('author_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('edit_comment_url'),
            pytest.lazy_fixture('reader_client'),
            NOT_FOUND,
        ),
        (
            pytest.lazy_fixture('delete_comment_url'),
            pytest.lazy_fixture('author_client'),
            OK,
        ),
        (
            pytest.lazy_fixture('delete_comment_url'),
            pytest.lazy_fixture('reader_client'),
            NOT_FOUND,
        ),
    ),
)
def test_page_availability_for_users(url, user_client, status_code):
    response = user_client.get(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    'name_url',
    (
        (pytest.lazy_fixture('edit_comment_url')),
        (pytest.lazy_fixture('delete_comment_url')),
    ),
)
def test_redirect_edit_delete_for_anonymous(name_url, client, login_url):
    expected_url = f'{login_url}?next={name_url}'
    response = client.get(name_url)
    assertRedirects(response, expected_url)
